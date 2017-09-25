# 弹药

import requests
from bs4 import BeautifulSoup, Tag
import json
from gamesky.base import BaseItem
from util import headers

base_url = 'http://pubg.ali213.net/pubg/items'

ammo = 'ammo'
big_category = ammo


class Ammo(BaseItem):
    def __init__(self) -> None:
        super().__init__(big_category, ammo)


def fetch_text(type):
    r = requests.get(base_url + '/' + type, headers=headers)
    print('url:{}'.format(base_url + '/' + type))
    r.encoding = 'utf-8'
    return r.text


def process(small_category):
    print('---> start {}'.format(big_category))
    print('small category : {}'.format(small_category))

    text = fetch_text(ammo)
    dom = BeautifulSoup(text, 'html.parser')
    div_block = dom.find('div', 'card-block large-item-block')  # type:Tag
    div_item = div_block.find_all('div', 'col-12 col-lg-6')
    list_ammo=[]
    for div in div_item:
        a=Ammo()
        a.name=div.find('div','media-body').contents[0].text
        a.summary=div.find('div','media-body').contents[1].text
        a.avatar_url=div.find('img')['src']
        list_ammo.append(a)
    return list_ammo



list_ammo=process(ammo)
print(json.dumps(list_ammo,default=lambda obj:obj.to_json,ensure_ascii=False))
