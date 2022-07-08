import requests
# from pprint import pprint

name = input('Введите имя пользователя у которого ищите репозитории: ')

url = 'https://api.github.com/search/users?q=' + name

response = requests.get(url)

j_data = response.json()

user_name = j_data.get('items')[0].get('login')

repos_url = j_data.get('items')[0].get('repos_url')
response = requests.get(repos_url)
j_data = response.json()

print(f"Ник пользователя : {user_name}")
for i in j_data:
    print(f" репозиторий ---- {i.get('name')}")
