# -*- coding: utf-8 -*-

import datetime
import logging
from typing import List

from peewee import *
from peewee import SelectQuery

logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

db = SqliteDatabase('my_database.db')


class BaseMode(Model):
    created_date = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Box(BaseMode):
    title = CharField()
    pic_name = CharField(null=True)


class Question(BaseMode):
    pic_name = CharField(null=True)
    q = CharField()  # ["顶叶","枕叶","岛叶","额叶","颞叶"]
    a = IntegerField()  # 3
    box = ForeignKeyField(Box, related_name='questions')


def get_boxs() -> SelectQuery:
    return Box.select()


def get_questions_by_boxid(boxid: int) -> List[Question]:
    box = Box.get(Box.id == boxid)
    if box:
        return box.questions


def init_db():
    db.create_tables([Box, Question], safe=True)


def clear_db():
    Question.delete().execute()
    Box.delete().execute()

init_db()