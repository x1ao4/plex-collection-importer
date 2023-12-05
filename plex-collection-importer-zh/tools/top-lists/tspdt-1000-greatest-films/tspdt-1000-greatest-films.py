import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 如果需要获取 TMDB ID 请在这里填写您的 TMDB API 密钥，如果不需要就保持为空字符串
tmdb_api_key = ""

def get_tmdb_id(title, year, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}&year={year}"
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url)
        if response.status_code != 200:
            return ''
        data = response.json()
        if data['results']:
            return data['results'][0]['id']
        else:
            return ''
    except requests.exceptions.RequestException as e:
        return ''

def get_movie_info(url, tmdb_api_key=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('tr', class_=re.compile('csv_row'))

    for movie in movie_list:
        columns = movie.find_all('td')
        rank = columns[0].text
        title = columns[2].text

        if ',' in title:
            parts = title.split(', ')
            if parts[1] == "L'":
                title = parts[1] + parts[0]
            else:
                title = ' '.join(parts[::-1])
        year = columns[4].text
        tmdb_id = ''
        if tmdb_api_key:
            tmdb_id = get_tmdb_id(title, year, tmdb_api_key)
            if tmdb_id:
                tmdb_id = f' {{tmdb-{tmdb_id}}}'
        movie_info = f'{rank} {title} ({year}){tmdb_id}'
        print(movie_info)
        with open('TSPDT 1,000 Greatest Films.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')

url = 'https://www.theyshootpictures.com/gf1000_all1000films_table.php'

file_path = 'TSPDT 1,000 Greatest Films.txt'
if os.path.exists(file_path):
    os.remove(file_path)

get_movie_info(url, tmdb_api_key)
