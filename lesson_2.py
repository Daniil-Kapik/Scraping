from itertools import count
import requests
from bs4 import BeautifulSoup
from pprint import pprint

page = 0
headers = {'User-Agent':
           'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}
mane_url = 'https://hh.ru'


def get_salary(salary_field):
    salary = {'min': None, 'max': None, 'currency': None}
    if salary_field:
        salary_replace = salary_field.text.replace('\u202f', '').split(' ')
        if salary_replace[0] == 'от':
            salary['min'] = int(salary_replace[1])
        elif salary_replace[0] == 'до':
            salary['max'] = int(salary_replace[1])
        else:
            salary['min'] = int(salary_replace[0])
            salary['max'] = int(salary_replace[2])
        salary['currency'] = salary_replace[-1]
    return salary


vacancies_data = []
count = 1
while True:
    url = 'https://hh.ru/search/vacancy'
    params = {'page': page, 'search_field': [
        'name', 'company_name', 'description'], 'text': 'Python'}

    session = requests.Session()
    response = session.get(url=url, headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', class_='vacancy-serp-item-body')

    pagers = dom.find('div', class_='pager').find(
        'a', {'data-qa': 'pager-next'})
    if not pagers:
        break

    pprint(f"загрузка страницы -- {count}")
    vacancies_data = []
    for vacancy in vacancies:
        vacancies_dict = {}
        title_href = vacancy.find('a', class_='bloko-link')
        vacancies_dict['name'] = title_href.text
        vacancies_dict['site'] = mane_url
        vacancies_dict['link_vacancy'] = title_href.get('href')
        vacancies_dict['salary'] = get_salary(vacancy.find(
            'span', {'data-qa': 'vacancy-serp__vacancy-compensation'}))
        vacancies_data.append(vacancies_dict)
    count += 1
    page += 1


pprint(vacancies_data)
