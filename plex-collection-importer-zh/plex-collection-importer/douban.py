import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_tmdb_id(title, year, api_key, media_type):
    url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={title}&year={year}&language=zh-CN"
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url)
        if response.status_code != 200:
            return ''
        data = response.json()
        if data['results']:
            result = data['results'][0]
            return result['id']
        return ''
    except requests.exceptions.RequestException as e:
        return ''

def get_movie_info(url, start, tmdb_api_key=None, media_type='movie', first_page=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.douban.com/',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return 0, None
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('div', class_='doulist-item')
    list_name = soup.find('h1').text.strip()

    invalid_chars = ':*?"<>|/'
    for char in invalid_chars:
        list_name = list_name.replace(char, '')

    file_path = f'../downloads/{list_name}.txt'
    if first_page:
        print(f'正在获取片单：{list_name}\n')
        if os.path.exists(file_path):
            os.remove(file_path)

    file_mode = 'w' if first_page else 'a'

    for movie in movie_list:
        title_div = movie.find('div', class_='title')
        if title_div is None:
            continue
        title = title_div.text.strip()
        if ' ' not in title:
            title = title
        elif title.count(' ') == 1:
            title = title.split(' ')[0]
        else:
            title_match = re.search(r'^[^\s]*[^\u4e00-\u9fa5\s]*[\u4e00-\u9fa5]+[^\s]*', title)
            if title_match is None:
                title_match = re.search(r'^.*?(?=\s[^a-zA-Z]|$)', title)
            title = title_match.group()
        details = movie.find('div', class_='abstract').text.strip()
        year_match = re.search(r'\d{4}', details)
        year = year_match.group() if year_match else ''
        rank = start + movie_list.index(movie) + 1
        tmdb_id = ''
        if tmdb_api_key:
            tmdb_id = get_tmdb_id(title, year, tmdb_api_key, media_type)
            if tmdb_id:
                tmdb_id = f' {{tmdb-{tmdb_id}}}'
        movie_info = f'{rank} {title} ({year}){tmdb_id}'
        print(movie_info)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')

    next_page_link = soup.find('a', string='后页>')
    return len(movie_list), next_page_link and next_page_link.get('href'), list_name

def main(list_id, tmdb_api_key):
    media_type = input("请输入片单的类型（movie或tv）：") if tmdb_api_key else None
    print()
    base_url = f'https://www.douban.com/doulist/{list_id}/?start='

    i = 0
    list_name = None
    while True:
        url = base_url + str(i * 25)
        count, has_next_page, name = get_movie_info(url, i * 25, tmdb_api_key, media_type, i == 0)
        if list_name is None:
            list_name = name
        if not has_next_page:
            break
        i += 1
        time.sleep(2)
    return list_name
