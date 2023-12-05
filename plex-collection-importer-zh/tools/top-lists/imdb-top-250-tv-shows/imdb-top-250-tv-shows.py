import os
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_tv_show_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    tv_show_list = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-59b6048d-0 cuaJSp cli-parent')

    for tv_show in tv_show_list:
        rank = tv_show.find('h3').text.split('.')[0]
        title = tv_show.find('h3').text.split('.')[1].strip()
        year = tv_show.find('span', class_='sc-479faa3c-8 bNrEFi cli-title-metadata-item').text
        if '–' in year:
            year = year.split('–')[0]
        imdb_id = tv_show.find('a')['href'].split('/')[2]
        tv_show_info = f'{rank} {title} ({year}) {{imdb-{imdb_id}}}'
        print(tv_show_info)
        with open('IMDb Top 250 TV Shows.txt', 'a', encoding='utf-8') as f:
            f.write(tv_show_info + '\n')

url = 'https://www.imdb.com/chart/toptv/'

file_path = 'IMDb Top 250 TV Shows.txt'
if os.path.exists(file_path):
    os.remove(file_path)

get_tv_show_info(url)
