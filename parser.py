import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://alfa.kz/phones/telefony-i-smartfony/page{}#products'

result_phones = []


def parse_phone(phone_url):
    response = requests.get(phone_url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find('h1', {'itemprop': 'name'}).text
    price = soup.find('span', {'class': 'num'}).text.replace(' ', '')
    seller = soup.find('div', {'class': 'panel-body'}).find('a').text.strip()

    description = soup.find_all('div', {'id': 'additional-info'})
    for feature in description:
        ram = feature.find('dt', {'title': 'Оперативная память'}).find_next().string.strip()
        memory = feature.find('dt', {'title': 'Встроенная память'}).find_next().string.strip()
    return title, price, seller, ram, memory


for page in range(2):
    response = requests.get(URL.format(page))
    soup = BeautifulSoup(response.text, "html.parser")
    phones = soup.find_all("div", {"class": "row product-item product-item-holder"})
    for phone in phones:
        try:
            phone_url = phone.find('div', {'class': 'title'}).find('a')['href']
        except:
            continue
        title, price, seller, ram, memory = parse_phone(phone_url)
        phone_dict = {'title': title, 'price': price, 'seller': seller, 'ram': ram, 'memory': memory}
        result_phones.append(phone_dict)
        if len(result_phones) == 10:
            break

keys = result_phones[0].keys()

with open('phones.csv', 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result_phones)
