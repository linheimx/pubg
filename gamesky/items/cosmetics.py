# 弹药

import json

import requests
from bs4 import BeautifulSoup, Tag

from gamesky.base import BaseItem
from util import headers

base_url = 'http://pubg.ali213.net/pubg/items'

cosmetics = 'cosmetics'
big_category = cosmetics

headgear = 'headgear'
eyewear = 'eyewear'
mask = 'mask'
shirt = 'shirt'
jacket = 'jacket'
glove = 'glove'
bottom = 'bottom'
footwear = 'footwear'

smalls = []
smalls.extend((headgear, eyewear, mask, shirt, jacket, glove, bottom, footwear))


class Cosmetics(BaseItem):
    def __init__(self, small_category) -> None:
        super().__init__(big_category, small_category)


def fetch_text(type):
    r = requests.get(base_url + '/' + type, headers=headers)
    print('url:{}'.format(base_url + '/' + type))
    r.encoding = 'utf-8'
    return r.text


def process():
    print('---> start {}'.format(big_category))
    print('big category : {}'.format(big_category))

    text = fetch_text(cosmetics)
    dom = BeautifulSoup(text, 'html.parser')
    div_items = dom.find_all('div', 'card item-card')  # type:Tag

    kv = {}
    for index, div_item in enumerate(div_items):
        div = div_item.find_all('div', 'col-12 col-md-6 col-lg-4')
        key = smalls[index]
        kv[key] = process_item(key, div)

    return kv


def process_item(small_category, div_item):
    list_cos = []
    for div in div_item:
        a = Cosmetics(small_category)
        a.name = div.find('div', 'media-body').contents[0].text
        a.avatar_url = div.find('img')['src']
        list_cos.append(a)
    return list_cos


kv = process()
print(json.dumps(kv, default=lambda obj: obj.to_json, ensure_ascii=False))
