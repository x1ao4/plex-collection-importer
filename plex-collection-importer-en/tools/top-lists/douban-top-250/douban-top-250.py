import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# If you need to fetch TMDB ID, please enter your TMDB API key here, Leave it blank if not needed
tmdb_api_key = ""

def get_tmdb_id(title, year, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}&year={year}&language=zh-CN"
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
    movie_list = soup.find_all('div', class_='item')

    for movie in movie_list:
        rank = movie.find('em').text
        title = movie.find('span', class_='title').text
        details = movie.find('p', class_='').text.strip()
        year_match = re.search(r'\d{4}', details)
        year = year_match.group() if year_match else ''
        tmdb_id = ''
        if tmdb_api_key:
            tmdb_id = get_tmdb_id(title, year, tmdb_api_key)
            if tmdb_id:
                tmdb_id = f' {{tmdb-{tmdb_id}}}'
        movie_info = f'{rank} {title} ({year}){tmdb_id}'
        print(movie_info)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')

base_url = 'https://movie.douban.com/top250?start={}&filter='

file_path = 'DOUBAN Top 250 Movies.txt'
if os.path.exists(file_path):
    os.remove(file_path)

for i in range(10):
    url = base_url.format(i * 25)
    get_movie_info(url, tmdb_api_key)
