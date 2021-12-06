import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://clutch.co/web-designers/research'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', 'accept': '*/*'}
HOST = 'https://clutch.co'
FILE = 'service.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='page-link')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='provider-row')

    service = []
    for item in items:





        service.append({
            'title': item.find('h3', class_='company-name').get_text(strip=True),
            'link': HOST + item.find('div', class_='company_logotype').find_next('a').get('href'),
            'project-size': item.find('div', class_='list-item').get_text(strip=True),
            'hourly-rate': item.find('i', class_='icon_clock').find_next('span').get_text(strip=True),
            'employees': item.find('i', class_='icon_person').find_next('span').get_text(strip=True),
            'location': item.find('i', class_='icon_pin').find_next('span').get_text(strip=True),
            'reviews': item.find('div', class_='grid').get_text(strip=True).replace('.', ','),
            'clients-experience': item.find('div', class_='grid').find_next('div', {"data-pos": "2"}).get_text(strip=True).replace('.', ','),
            'market-presence': item.find('div', class_='grid').find_next('div', {"data-pos": "3"}).get_text(strip=True).replace('.', ','),
            'sum-of-deliver': item.find('label', class_='sum').get_text(strip=True).replace('.', ','),
            'web-design': item.find('div', class_='value custom_popover').get_text(strip=True),
            # 'other': item.find('div', class_='grid custom_popover grid-transparent').get_text(strip=True),
        })
    return service
        


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link', 'project-size', 'hourly-rate', 'employees', 'location', 'reviews',
                        'clients-experience', 'market-presence', 'sum-of-deliver', 'web-design'])
        for item in items:
            writer.writerow([item['title'],
                             item['link'],
                             item['project-size'],
                             item['hourly-rate'],
                             item['employees'],
                             item['location'],
                             item['reviews'],
                             item['clients-experience'],
                             item['market-presence'],
                             item['sum-of-deliver'],
                             item['web-design'],
                             ])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        service = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page - 1})
            service.extend(get_content(html.text))
            save_file(service, FILE)
        print(f'Получено {len (service)} карточек')
        os.startfile(FILE)
    else:
        print('Error')


parse()
