import os
import requests
from bs4 import BeautifulSoup
import time
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# If you need to fetch TMDB ID, please enter your TMDB API key here, Leave it blank if not needed
tmdb_api_key = ""

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

def get_movie_info(url, start, tmdb_api_key=None, media_type='movie'):
    response = requests.get(url)
    if response.status_code != 200:
        return 0, None
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.find_all('div', class_='grid-item')
    
    list_name_element = soup.find('meta', itemprop='name')
    list_name = list_name_element.get('content').strip()

    invalid_chars = ':*?"<>|/'
    for char in invalid_chars:
        list_name = list_name.replace(char, '')

    file_path = f'{list_name}.txt'
    if start == 0 and os.path.exists(file_path):
        os.remove(file_path)

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
        with open(f'{list_name}.txt', 'a', encoding='utf-8') as f:
            f.write(movie_info + '\n')
    next_page_link = soup.find('li', class_='next')
    if next_page_link is None or 'disabled' in next_page_link.get('class'):
        return len(movie_list), None
    else:
        return len(movie_list), next_page_link.find('a').get('href')

username, list_id = input("Please enter Trakt list username and list ID (separated by space): ").split()
media_type = input("Please enter the type of the list (movie or tv): ") if tmdb_api_key else None
print()
base_url = f'https://trakt.tv/users/{username}/lists/{list_id}?page='

i = 1
total = 0
while True:
    url = base_url + str(i) + '&sort=rank,asc'
    count, has_next_page = get_movie_info(url, total, tmdb_api_key, media_type)
    total += count
    if has_next_page is None:
        break
    i += 1
    time.sleep(2)
