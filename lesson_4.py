from lxml import html
import requests
from pprint import pprint

header = {
    'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}

url = 'https://news.mail.ru'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath(
    ".//table[@class='daynews__inner']//td[position()<3]/div[position()<3]/a/@href"
    "|"
    ".//ul[@class='list list_type_square list_half js-module']/li/a/@href")
print(len(items))

mail_news_data = []
for item in items:
    respon = session.get(item, headers=header)
    dom = html.fromstring(respon.text)

    mail_news = {}
    date = dom.xpath(
        ".//div[contains(@class, 'cols__column_small_23')][2]//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    source = dom.xpath(
        ".//span[@class='breadcrumbs__item'][2]//a/span/text()")
    name = dom.xpath(
        ".//div[contains(@class, 'meta-speakable-title')]//h1/text()")
    text = dom.xpath(
        ".//div[@class='article__intro meta-speakable-intro']/p/text()")
    mail_news['name'] = name
    mail_news['text'] = text
    mail_news['date'] = date
    mail_news['source'] = source
    mail_news_data.append(mail_news)

pprint(mail_news_data)
