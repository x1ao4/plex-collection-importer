import os
import re
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import glob
import douban
import imdb
import trakt

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    if 'server' in config.sections():
        server = config.get('server', 'address')
        token = config.get('server', 'token')
        tmdb_api_key = config.get('server', 'tmdb_api_key')
        return server, token, tmdb_api_key
    else:
        return None, None, None

def choose_libraries(plex):
    print("以下是您的Plex服务器上的所有影视库：\n")
    libraries = [lib for lib in plex.library.sections() if lib.type in ['movie', 'show']]
    for i, library in enumerate(libraries, 1):
        print(f"{i}. {library.title}")
    choices = input("\n请输入您想选择的库的编号（多个编号请用空格隔开）：")
    print()
    choices = list(map(int, choices.split()))
    return [libraries[choice - 1] for choice in choices]

def get_movie_ids(movie):
    ids = {}
    for guid in movie.guids:
        if 'imdb' in guid.id:
            ids['imdb'] = guid.id.split('://')[1]
        elif 'tmdb' in guid.id:
            ids['tmdb'] = guid.id.split('://')[1]
        elif 'tvdb' in guid.id:
            ids['tvdb'] = guid.id.split('://')[1]

    xml_data = ET.tostring(movie._server.query(movie.key))
    root = ET.fromstring(xml_data)
    ids['collections'] = [elem.attrib['tag'] for elem in root.iter('Collection')]
    return ids

def clean_string(s):
    return re.sub(r'\W+', '', s)

def get_list(tmdb_api_key):
    list_id = input("请输入片单的ID：")
    if list_id.isdigit():
        list_name = douban.main(list_id, tmdb_api_key)
    elif list_id.startswith('ls'):
        list_name = imdb.main(list_id)
    elif ' ' in list_id:
        list_name = trakt.main(list_id, tmdb_api_key)
    else:
        return None
    return f"../downloads/{list_name}.txt"

def main():
    server, token, tmdb_api_key = read_config()
    plex = PlexServer(server, token)

    libraries = choose_libraries(plex)

    txt_files = glob.glob("../collections/*.txt")
    if not txt_files:
        txt_file = get_list(tmdb_api_key)
        if txt_file is None:
            print("\n无法识别片单ID，请在获取了正确的片单ID后重试")
            return
        txt_files = [txt_file]
    else:
        print("正在读取片单...\n")
        for txt_file in txt_files:
            print(os.path.splitext(os.path.basename(txt_file))[0])

    for library in libraries:
        print(f"\n正在匹配库：{library.title}\n")
        added_to_collection = False
        for txt_file in txt_files:
            collection_name = os.path.splitext(os.path.basename(txt_file))[0]
            with open(txt_file, "r", encoding="utf-8") as f:
                collection_movies = []
                for line in f:
                    match = re.match(r'\d+ (.+?) \((\d{4})\)(?: \{(.+?)-(.+?)\})?', line.strip())
                    if match:
                        title, year, platform, id = match.groups()
                        movie_info = (title, year)
                        if platform and id:
                            collection_movies.append((platform, id))
                        else:
                            collection_movies.append(movie_info)

            movies = library.all()
            for movie in movies:
                title = clean_string(movie.title)
                year = movie.year if movie.year else "未知"
                movie_info = (title, str(year))
                
                movie_ids = get_movie_ids(movie)
                if movie_info in map(lambda x: (clean_string(x[0]), x[1]), collection_movies):
                    if collection_name not in movie_ids['collections']:
                        print(f"\"{movie.title} ({year})\" 已被添加到 \"{collection_name}\" 合集中")
                        movie.addCollection(collection_name)
                        added_to_collection = True
                    if movie_info in collection_movies:
                        collection_movies.remove(movie_info)
                else:
                    for platform, id in collection_movies:
                        if platform in movie_ids and movie_ids[platform] == id:
                            if collection_name not in movie_ids['collections']:
                                print(f"\"{movie.title} ({year})\" 已被添加到 \"{collection_name}\" 合集中")
                                movie.addCollection(collection_name)
                                added_to_collection = True
                            if (platform, id) in collection_movies:
                                collection_movies.remove((platform, id))
                            break
        if not added_to_collection:
            print(f"没有在 \"{library.title}\" 中发现需要被添加至合集的项目")

if __name__ == '__main__':
    main()