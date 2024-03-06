import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_imdb_id(url):
    return url.split('/')[-2]

def get_movie_info(url, start):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return 0
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('div', class_='lister-item mode-simple')
    list_name = soup.find('h1').text.strip()

    invalid_chars = ':*?"<>|/'
    for char in invalid_chars:
        list_name = list_name.replace(char, '')

    file_path = f'{list_name}.txt'
    if start == 0 and os.path.exists(file_path):
        os.remove(file_path)

    for movie in movie_list:
        title_div = movie.find('div', class_='col-title')
        title = title_div.find('a').text.strip()
        year = title_div.find('span', class_='lister-item-year text-muted unbold').text.strip('()')
        if '–' in year:
            year = year.split('–')[0]
        imdb_id = get_imdb_id(title_div.find('a')['href'])
        rank = start + movie_list.index(movie) + 1
        movie_info = f'{rank} {title} ({year}) {{imdb-{imdb_id}}}'
        print(movie_info)
        with open(f'{list_name}.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')
    next_page_link = soup.find('a', class_='flat-button lister-page-next next-page')
    return len(movie_list), next_page_link and next_page_link.get('href')

list_id = input("请输入IMDb片单的ID：")
print()
base_url = f'https://www.imdb.com/list/{list_id}/?sort=list_order,asc&st_dt=&mode=simple&page='

i = 0
while True:
    url = base_url + str(i + 1)
    count, has_next_page = get_movie_info(url, i * 100)
    if not has_next_page:
        break
    i += 1
    time.sleep(2)
