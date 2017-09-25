# 弹药

import json

import requests
from bs4 import BeautifulSoup, Tag

from gamesky.base import BaseItem
from util import headers

base_url = 'http://pubg.ali213.net/pubg/items'

attachments = 'attachments'
big_category = attachments

muzzle = 'muzzle'
low_rail = 'low_rail'
up_rail = 'up_rail'
magazine = 'magazine'
stock = 'stock'

smalls = []
smalls.extend((muzzle, low_rail, up_rail, magazine, stock))


class Attachment(BaseItem):
    def __init__(self, small_category) -> None:
        super().__init__(big_category, small_category)
        self.content = ''  # content


def fetch_text(type):
    r = requests.get(base_url + '/' + type, headers=headers)
    print('url:{}'.format(base_url + '/' + type))
    r.encoding = 'utf-8'
    return r.text


def process():
    print('---> start {}'.format(big_category))
    print('big category : {}'.format(big_category))

    text = fetch_text(attachments)
    dom = BeautifulSoup(text, 'html.parser')
    div_items = dom.find_all('div', 'card item-card attachments-card')  # type:Tag

    kv = {}
    for index, div_item in enumerate(div_items):
        div = div_item.find_all('div', 'row item-attachment-row align-items-center')
        key = smalls[index]
        kv[key] = process_item(key, div)

    return kv


def process_item(small_category, div_item):
    list_cos = []
    for div in div_item:
        a = Attachment(small_category)
        a.name = div.find('div', 'media-body').contents[0].text
        a.summary = div.find('div', 'media-body').contents[1].text
        a.avatar_url = div.find('img')['src']

        d=div.find('div','col-md-4 col-lg-3 offset-lg-1 item-attachment-data')
        for child in d.contents:
            a.content+=child.text+'\n'
        list_cos.append(a)
    return list_cos


kv = process()
print(json.dumps(kv, default=lambda obj: obj.to_json, ensure_ascii=False))
