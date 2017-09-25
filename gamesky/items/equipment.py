import json

import requests
from bs4 import BeautifulSoup, Tag

from gamesky.base import BaseItem
from util import headers

base_url = 'http://pubg.ali213.net/pubg/items'

big_category = 'equipment'
small = []

headgear = 'headgear'
armedvest = 'armedvest'
belt='belt'
outer='outer'
back='back'

small.append(headgear)
small.append(armedvest)
small.append(belt)
small.append(outer)
small.append(back)


class Equipment(BaseItem):
    def __init__(self, small_category: str) -> None:
        super().__init__(big_category, small_category)


class HeadGear(Equipment):
    def __init__(self) -> None:
        super().__init__(headgear)
        self.damage_reduction = ''  # 伤害减免
        self.durability = ''  # 耐久度
        self.weight = ''  # 重量


class ArmoredVest(Equipment):
    def __init__(self) -> None:
        super().__init__(armedvest)
        self.capacity = ''  # 携带容量加成
        self.damage_reduction = ''  # 伤害减免
        self.durability = ''  # 耐久度
        self.weight = ''  # 重量

class Belt(Equipment):
    def __init__(self) -> None:
        super().__init__(belt)
        self.capacity = ''  # 携带容量加成
        self.damage_reduction = ''  # 伤害减免
        self.weight = ''  # 重量

class Outer(Equipment):
    def __init__(self) -> None:
        super().__init__(outer)
        self.capacity = ''  # 携带容量加成
        self.damage_reduction = ''  # 伤害减免
        self.weight = ''  # 重量

class Back(Equipment):
    def __init__(self) -> None:
        super().__init__(back)
        self.capacity = ''  # 携带容量加成
        self.weight = ''  # 重量

def fetch_text(type):
    r = requests.get(base_url + '/' + type, headers=headers)
    print('url:{}'.format(base_url + '/' + type))
    r.encoding = 'utf-8'
    return r.text


def process(small_category):
    print('---> start {}'.format(big_category))
    print('small category : {}'.format(small_category))

    text = fetch_text(big_category)
    dom = BeautifulSoup(text, 'html.parser')
    div_item = dom.find_all('div', 'card item-card')  # type:Tag

    list_eq = []
    if small_category == headgear:
        list_eq = process_headgear(div_item[0])
    elif small_category == armedvest:
        list_eq = process_armvest(div_item[1])
    elif small_category == belt:
        list_eq = process_belt(div_item[2])
    elif small_category == outer:
        list_eq = process_outer(div_item[3])
    elif small_category == back:
        list_eq = process_back(div_item[4])

    return list_eq


def process_headgear(div_item):
    tbody = div_item.find('tbody')
    trs = tbody.find_all('tr')

    list_headgear = []
    for tr in trs:
        children = tr.contents
        item = HeadGear()
        item.name = children[0].text
        item.avatar_url = children[0].find('img')['src']
        item.summary = ''

        item.damage_reduction = children[1].text
        item.durability = children[2].text
        item.weight = children[3].text
        list_headgear.append(item)
    return list_headgear

def process_armvest(div_item):
    tbody = div_item.find('tbody')
    trs = tbody.find_all('tr')

    list_armvest = []
    for tr in trs:
        children = tr.contents
        item = ArmoredVest()
        item.name = children[0].text
        item.avatar_url = children[0].find('img')['src']
        item.summary = ''

        item.capacity = children[1].text
        item.damage_reduction = children[2].text
        item.durability = children[3].text
        item.weight = children[4].text
        list_armvest.append(item)
    return list_armvest

def process_belt(div_item):
    tbody = div_item.find('tbody')
    trs = tbody.find_all('tr')

    list_armvest = []
    for tr in trs:
        children = tr.contents
        item = Belt()
        item.name = children[0].text
        item.avatar_url = children[0].find('img')['src']
        item.summary = ''

        item.capacity = children[1].text
        item.damage_reduction = children[2].text
        item.weight = children[3].text
        list_armvest.append(item)
    return list_armvest

def process_outer(div_item):
    tbody = div_item.find('tbody')
    trs = tbody.find_all('tr')

    list_armvest = []
    for tr in trs:
        children = tr.contents
        item = Outer()
        item.name = children[0].text
        item.avatar_url = children[0].find('img')['src']
        item.summary = ''

        item.capacity = children[1].text
        item.damage_reduction = children[2].text
        item.weight = children[3].text
        list_armvest.append(item)
    return list_armvest

def process_back(div_item):
    tbody = div_item.find('tbody')
    trs = tbody.find_all('tr')

    list_armvest = []
    for tr in trs:
        children = tr.contents
        item = Back()
        item.name = children[0].text
        item.avatar_url = children[0].find('img')['src']
        item.summary = ''

        item.capacity = children[1].text
        item.weight = children[2].text
        list_armvest.append(item)
    return list_armvest


list_eq = []
for s in small:
    list_eq.append(process(s))

print(json.dumps(list_eq, default=lambda obj: obj.to_json, ensure_ascii=False))
