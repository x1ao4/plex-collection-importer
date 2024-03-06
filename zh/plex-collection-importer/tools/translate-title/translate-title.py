import os
import requests
import re
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 请在这里填写您的 TMDB API 密钥
tmdb_api_key = ""

# 设置片单的类型：'movie' 或 'tv'
media_type = 'movie'

# 设置匹配模式：'exact' 或 'fuzzy'
match_mode = 'fuzzy'

# 设置原始片单的语言：'zh-CN' 或 'en-US' 等
input_language = 'en-US'

# 设置输出片单的语言：'zh-CN' 或 'en-US' 等
output_language = 'zh-CN'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_tmdb_title(title, year, api_key):
    url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={title}&year={year}&language={input_language if match_mode == 'exact' else output_language}"
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return ''
    data = response.json()
    results = data.get('results')
    if results:
        if match_mode == 'exact':
            for result in results:
                if result.get('title') == title and result.get('release_date', '').startswith(str(year)):
                    id = result.get('id')
                    url = f"https://api.themoviedb.org/3/{media_type}/{id}?api_key={api_key}&language={output_language}"
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        return data.get('title') or data.get('name')
        else:
            return results[0].get('title') or results[0].get('name')
    return ''

def translate_title(file_path, tmdb_api_key):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_file_path = file_path.replace('.txt', f'-{output_language.split("-")[0].upper()}.txt')
    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    for line in lines:
        match = re.match(r'(\d+)\s+(.*?)\s+\((\d{4})\)(?:\s+\{(.*?)\})?', line.strip())
        if match:
            rank, title, year, extra = match.groups()
            translated_title = get_tmdb_title(title, year, tmdb_api_key)
            if translated_title:
                new_line = f'{rank} {translated_title} ({year})' + (f' {{{extra}}}' if extra else '')
            else:
                new_line = f'{rank} {title} ({year})' + (f' {{{extra}}}' if extra else '')
            print(new_line)
            with open(new_file_path, 'a', encoding='utf-8') as f:
                f.write(new_line + '\n')
            time.sleep(1)
    print()

def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(directory):
        if filename.endswith('.txt') and not filename.endswith(f'-{output_language.split("-")[0].upper()}.txt'):
            file_path = os.path.join(directory, filename)
            translate_title(file_path, tmdb_api_key)

if __name__ == "__main__":
    main()
