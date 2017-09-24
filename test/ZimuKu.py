import re

from typing import List
from bs4 import Tag
from bs4 import BeautifulSoup
import requests

base_url = 'http://www.zimuku.net'


class Movie:
    def __init__(self) -> None:
        super().__init__()
        self.name = ""
        self.detail_url = ""


class Zimu:
    def __init__(self) -> None:
        super().__init__()
        self.name = ""
        self.detail_url = ""


def get_MovieList(keyword: str) -> List[Movie]:
    '''
    根据关键字返回一堆电影信息
    :param keyword:
    :return:
    '''
    r = requests.get(base_url + '/search?ad=1&q={0}'.format(keyword))

    dom = BeautifulSoup(r.text, 'html.parser')

    list_movie = []

    div_blocks = dom.find_all('div', class_='item prel clearfix')
    try:
        for div_block in div_blocks:  # type:Tag
            movie = get_Movie(div_block)
            if movie:
                list_movie.append(movie)
    except BaseException:
        pass
    return list_movie


def get_Movie(item: Tag) -> Movie:
    '''
    解析一部电影
    :param item:
    :return:
    '''

    try:
        movie = Movie()

        a = item.select_one('div.title p a')  # type:Tag
        movie.detail_url = a['href']
        movie.name = a.findChild().text
    except BaseException:
        pass

    return movie


def get_ZimusByMovie(url: str) -> List[Zimu]:
    r = requests.get(base_url + "/" + url)
    dom = BeautifulSoup(r.text, 'html.parser')

    list_zimu = []

    father = dom.select_one('body tbody')  # type: Tag
    trs = father.select('tr')  # type:List[Tag]
    for tr in trs:
        try:
            a = tr.select_one('td a')
            zimu = Zimu()
            zimu.detail_url = a['href']
            zimu.name = a['title']
            list_zimu.append(zimu)
        except BaseException:
            continue
    return list_zimu


def get_DownloadUrl(detail_url: str):
    '''
    获取字幕的下载地址
    :param detail_url: 
    :return str: 
    '''
    r = requests.get(base_url + '/' + detail_url)
    hitUrl = re.findall(re.compile('/download/\w*"(?=>)'), r.text)[0]
    hitUrl = base_url + hitUrl
    return hitUrl


def download_Zimu(url: str, filename: str):
    '''
    下载字幕
    :param url: 
    :return: 
    '''
    # print('download:' + url)
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)


'''-------------------------> go <----------------------------'''

if __name__ == '__main__':
    # step1
    movie = input("请输入电影名称:")
    list_movie = get_MovieList(movie)

    for index, movie in enumerate(list_movie):
        print(index, movie.name)

    # step2
    try:
        index = int(input('请输入电影的下标'))
    except BaseException:
        exit(-1)

    if index >= 0 and index < list_movie.__sizeof__():
        print('--->：' + list_movie[index].name)
        movie = list_movie[index]
        list_zimu = get_ZimusByMovie(movie.detail_url)
        for index, zimu in enumerate(list_zimu):
            print(index, zimu.name)

    # step3
    try:
        index = int(input('请输入字幕的下标:'))
    except BaseException:
        exit(-1)

    if index >= 0 and index < list_zimu.__sizeof__():
        print('--->：' + list_zimu[index].name)
        url = get_DownloadUrl(list_zimu[index].detail_url)
        download_Zimu(url, zimu.name)
        print("下载完成")
