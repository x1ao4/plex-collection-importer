import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_tmdb_id(title, year, api_key, media_type):
    url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={title}&year={year}"
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
    response = requests.get(url)
    if response.status_code != 200:
        return 0, None, None
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('div', class_='grid-item')
    
    list_name_element = soup.find('meta', itemprop='name')
    list_name = list_name_element.get('content').strip()

    invalid_chars = ':*?"<>|/'
    for char in invalid_chars:
        list_name = list_name.replace(char, '')

    file_path = f'../downloads/{list_name}.txt'
    if first_page:
        print(f'Fetching list: {list_name}\n')
        if os.path.exists(file_path):
            os.remove(file_path)

    file_mode = 'w' if first_page else 'a'

    for movie in movie_list:
        rank = movie.get('data-rank')
        title = movie.find('h3', class_='ellipsify').text.strip()
        year = movie.get('data-released')[:4]
        tmdb_id = ''
        if tmdb_api_key:
            tmdb_id = get_tmdb_id(title, year, tmdb_api_key, media_type)
            if tmdb_id:
                tmdb_id = f' {{tmdb-{tmdb_id}}}'
        movie_info = f'{rank} {title} ({year}){tmdb_id}'
        print(movie_info)
        with open(f'../downloads/{list_name}.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')

    next_page_link = soup.find('li', class_='next')
    if next_page_link is None or 'disabled' in next_page_link.get('class'):
        return len(movie_list), None, list_name
    else:
        return len(movie_list), next_page_link.find('a').get('href'), list_name

def main(list_id, tmdb_api_key):
    username, list_id = list_id.split()
    media_type = input("Please enter the type of the list (movie or tv): ") if tmdb_api_key else None
    print()
    base_url = f'https://trakt.tv/users/{username}/lists/{list_id}?page='

    i = 1
    total = 0
    first_page = True
    while True:
        url = base_url + str(i) + '&sort=rank,asc'
        count, has_next_page, list_name = get_movie_info(url, total, tmdb_api_key, media_type, first_page)
        total += count
        if has_next_page is None:
            break
        i += 1
        first_page = False
        time.sleep(2)
    return list_name
