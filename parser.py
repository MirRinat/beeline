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
for i in range(2):
    response = requests.get(URL.format(i))
    soup = BeautifulSoup(response.text, "html.parser")
    phones = soup.find_all("div", {"class": "row product-item product-item-holder"})
    # print(len(phones))
    for phone in phones:
        try:
            title = phone.find('div', {'class': 'title'}).findChildren('h2').
        except:
            print('no')
            continue
        print(title)


# print(phones)