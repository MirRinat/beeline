import requests
from bs4 import BeautifulSoup
import re


URL = 'https://alfa.kz/phones/telefony-i-smartfony/page{}#products'


phone_dict = {'title': '',
              'price': '',
              'seller': '',
              'ram': '',
              'memory': ''}

result_phones = []

def parse_phone(phone_url):
    response = requests.get(phone_url)
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find_all('div', {'id': 'additional-info'})
    for feature in description:
        ram = feature.find('dt', {'title': 'Оперативная память'}).find_next().string.strip()
        memory = feature.find('dt', {'title': 'Встроенная память'}).find_next().string.strip()
    return ram, memory

for page in range(1):
    response = requests.get(URL.format(page))
    soup = BeautifulSoup(response.text, "html.parser")
    phones = soup.find_all("div", {"class": "row product-item product-item-holder"})
    for phone in phones:
        try:
            title = phone.find('div', {'class': 'title'}).findChildren('h2')[0].text
            phone_url = phone.find('div', {'class': 'title'}).find('a')['href']
        except:

            continue
        price = phone.find('div', {'class': 'price'}).find('span', {'class':'num'}).text
        seller = phone.find('div', {'class': 'alfa-seller vertical-center'}).find_all('a')[1].text
        ram, memory = parse_phone(phone_url)

        # description = phone.find('div', {'class': 'excerpt'}).find('p', {'itemprop': 'description'}).text.strip()

        # ram = re.search('Оперативная память:(.*),',description)
        # ram = ram.group(1)
        # print(phone_url)
        print(title,price,seller,ram, memory)


        # print(phone_url)
        # print(description)



# print(phones)