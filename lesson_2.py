from itertools import count
import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from pymongo import errors
from pprint import pprint
import json

client = MongoClient('127.0.0.1', 27017)
db = client['hh_user']
col_vacancies = db.vacancies

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


count = 1
while True:
    url = 'https://hh.ru/search/vacancy'
    params = {'page': page, 'search_field': [
        'name', 'company_name', 'description'], 'text': 'Python', 'items_on_page': 20}

    session = requests.Session()
    response = session.get(url=url, headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', class_='vacancy-serp-item-body')

    pagers = dom.find('div', class_='pager').find(
        'a', {'data-qa': 'pager-next'})
    if not pagers:
        break

    pprint(f"загрузка страницы -- {count}")
    for vacancy in vacancies:
        vacancies_dict = {}
        title_href = vacancy.find('a', class_='bloko-link')
        vacancies_dict['name'] = title_href.text
        vacancies_dict['site'] = mane_url
        vacancies_dict['link_vacancy'] = title_href.get('href')
        get_salaries = get_salary(vacancy.find(
            'span', {'data-qa': 'vacancy-serp__vacancy-compensation'}))
        vacancies_dict['min'] = get_salaries['min']
        vacancies_dict['max'] = get_salaries['max']
        vacancies_dict['currency'] = get_salaries['currency']
        # ----------------------------------------------------------------------------------------
        col_vacancies.update_one({'link_vacancy': vacancies_dict['link_vacancy']}, {
            '$set': vacancies_dict}, upsert=True)
        # ----------------------------------------------------------------------------------------
    count += 1
    page += 1


def find_vacancies_for_salary(inp_salary: int, inp_currency: str):

    result = col_vacancies.find({
        '$and': [
            {'$or': [{'min': {'$gt': inp_salary}},
                     {'max': {'$gt': inp_salary}}]},
            # {'currency': 'руб'}
        ]
    })

    return list(result)


print(find_vacancies_for_salary(100000, 'руб'))
# db.vacancies.drop()
