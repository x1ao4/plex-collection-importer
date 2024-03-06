import os
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_movie_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-59b6048d-0 cuaJSp cli-parent')

    for movie in movie_list:
        rank = movie.find('h3').text.split('.')[0]
        title = movie.find('h3').text.split('.')[1].strip()
        year = movie.find('span', class_='sc-479faa3c-8 bNrEFi cli-title-metadata-item').text
        imdb_id = movie.find('a')['href'].split('/')[2]
        movie_info = f'{rank} {title} ({year}) {{imdb-{imdb_id}}}'
        print(movie_info)
        with open('IMDb Top 250 Movies.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')

url = 'https://www.imdb.com/chart/top/'

file_path = 'IMDb Top 250 Movies.txt'
if os.path.exists(file_path):
    os.remove(file_path)

get_movie_info(url)
