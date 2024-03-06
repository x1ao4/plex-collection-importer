import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 如果需要获取 TMDB ID 请在这里填写您的 TMDB API 密钥，如果不需要就保持为空字符串
tmdb_api_key = ""

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

def get_movie_info(url, start, tmdb_api_key=None, media_type='movie'):
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

    file_path = f'{list_name}.txt'
    if start == 0 and os.path.exists(file_path):
        os.remove(file_path)

    for movie in movie_list:
        title_div = movie.find('div', class_='title')
        if title_div is None:
            continue
        title = title_div.text.strip()
        if ' ' not in title:  # 如果标题中不包含空格
            title = title  # 直接使用原名
        elif title.count(' ') == 1:  # 如果标题中只有一个空格
            title = title.split(' ')[0]  # 保留空格前的所有内容
        else:  # 如果标题中包含多个空格
            title_match = re.search(r'^[^\s]*[^\u4e00-\u9fa5\s]*[\u4e00-\u9fa5]+[^\s]*', title)  # 保留第一个相邻字符中包含汉字的空格前的所有内容
            if title_match is None:  # 如果没有找到匹配的空格
                title_match = re.search(r'^.*?(?=\s[^a-zA-Z]|$)', title)  # 保留第一个相邻字符不全是英文字符的空格前的所有内容
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
        with open(f'{list_name}.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')
    next_page_link = soup.find('a', string='后页>')
    return len(movie_list), next_page_link and next_page_link.get('href')

list_id = input("请输入豆瓣片单的ID：")
media_type = input("请输入片单的类型（movie或tv）：") if tmdb_api_key else None
print()
base_url = f'https://www.douban.com/doulist/{list_id}/?start='

i = 0
while True:
    url = base_url + str(i * 25)
    count, has_next_page = get_movie_info(url, i * 25, tmdb_api_key, media_type)
    if not has_next_page:
        break
    i += 1
    time.sleep(2)
