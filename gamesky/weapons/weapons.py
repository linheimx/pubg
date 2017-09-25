import json

import requests
from bs4 import BeautifulSoup, Tag

from gamesky.base import BaseItem
from util import headers

base_url = 'http://pubg.ali213.net/pubg/weapons'
guns = ['sniper-rifles', 'assault-rifles', 'submachine-guns', 'shotguns', 'pistols', 'misc']
melee = 'melee'
throwable = 'throwables'

big_category = 'weapons'
small = list(guns)
small.append(melee)
small.append(throwable)


class Gun(BaseItem):
    def __init__(self, small_category: str):
        super().__init__(big_category, small_category)
        self.o_hit_damage = ''  # 命中伤害
        self.o_bullet_speed = ''  # 初始子弹速度
        self.o_hit_impact_power = ''  # 击中身体冲击力
        self.o_zero_range = ''  # 归零距离
        self.o_ammo_per_mag = ''  # 弹匣容量
        self.o_time_betw_shoots = ''  # 射击间隔
        self.o_fire_mode = ''  # 射击模式

        self.reload_duration_full = ''  # 装弹时间:持续时间（填满）

    def __str__(self) -> str:
        return 'name:{} summary:{} avatar_url:{}   ' \
               'o_hit_damage:{} o_bullet_speed:{} o_hit_impact_power:{} o_zero_range:{} o_ammo_per_mag:{} o_time_betw_shoots:{} o_fire_mode:{}' \
            .format(
            self.name, self.summary, self.avatar_url,
            self.o_hit_damage, self.o_bullet_speed, self.o_hit_impact_power, self.o_zero_range, self.o_ammo_per_mag,
            self.o_time_betw_shoots, self.o_fire_mode)


class Melee(BaseItem):
    def __init__(self) -> None:
        super().__init__(big_category, melee)
        self.o_hit_damage = ''  # 命中伤害
        self.o_hit_range_leeway = ''  # 击打范围？

        self.pick_duration = ''  # 捡拾延时


class THrowable(BaseItem):
    def __init__(self) -> None:
        super().__init__(big_category, throwable)
        self.pickup_delay = ''  # 投掷延时
        self.ready_delay = ''  # 准备延时
        self.active_time_limit = ''  # 激活时间


def fetch_text(type):
    r = requests.get(base_url + '/' + type, headers=headers)
    print('url:{}'.format(base_url + '/' + type))
    r.encoding = 'utf-8'
    return r.text


def process(small_category):
    print('---> start {}'.format(small_category))

    text = fetch_text(small_category)
    dom = BeautifulSoup(text, 'html.parser')
    father = dom.find('div', 'card-block stat-comparison weapon-comparison')  # type:Tag
    children_row = father.contents

    row_header = children_row[0]
    cols = row_header.find_all('div', class_='col')
    list_weapon = []
    for i, col in enumerate(cols):
        if small_category == melee:
            w = Melee()
        elif small_category == throwable:
            w = THrowable()
        else:
            w = Gun(small_category)

        w.avatar_url = col.find('img')['src']

        div = col.find('div', class_='item-header')
        w.name = div.find('h3').text
        w.summary = div.find('p').text

        if small_category == melee:
            process_overview_melee(w, children_row[1], i)
        elif small_category == throwable:
            process_overview_throwable(w, children_row[1], i)
        else:
            process_overview_gun(w, children_row[1], i)

        list_weapon.append(w)

    return list_weapon


def process_overview_gun(gun, div_over: Tag, index):
    div_v_block = div_over.contents[index]  # type:Tag

    gun.o_hit_damage = div_v_block.find('div', text='命中伤害').previous_sibling.text
    gun.o_bullet_speed = div_v_block.find('div', text='初始子弹速度').previous_sibling.text
    gun.o_hit_impact_power = div_v_block.find('div', text='击中身体冲击力').previous_sibling.text
    gun.o_zero_range = div_v_block.find('div', text='归零距离').previous_sibling.text
    gun.o_ammo_per_mag = div_v_block.find('div', text='弹匣容量').previous_sibling.text
    gun.o_time_betw_shoots = div_v_block.find('div', text='射击间隔').previous_sibling.text
    gun.o_fire_mode = div_v_block.find('div', text='射击模式').previous_sibling.text

    gun.reload_duration_full = div_v_block.find('div', text='持续时间（填满）').previous_sibling.text


def process_overview_melee(melee, div_over: Tag, index):
    div_v_block = div_over.contents[index]  # type:Tag

    melee.o_hit_damage = div_v_block.find('div', text='Damage').previous_sibling.text
    melee.o_hit_range_leeway = div_v_block.find('div', text='Hit 范围 Leeway').previous_sibling.text

    div_other = div_over.next_sibling
    melee.pick_duration = div_other.find('div', text='捡拾延时').previous_sibling.text


def process_overview_throwable(throwable, div_over: Tag, index):
    div_v_block = div_over.contents[index]  # type:Tag

    throwable.active_time_limit = div_v_block.find('div', text='Activation Time Limit').previous_sibling.text

    div_other = div_over.next_sibling
    throwable.pickup_delay = div_other.find('div', text='投掷延时').previous_sibling.text
    throwable.ready_delay = div_other.find('div', text='准备延时').previous_sibling.text


list_weapon = []
for w in small:
    list_weapon.append(process(w))

print(json.dumps(list_weapon, default=lambda obj: obj.to_json, ensure_ascii=False))
