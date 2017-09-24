

class BaseItem(object):
    def __init__(self, big_category: str, small_category: str) -> None:
        self.big_category = big_category  # big 类
        self.small_category = small_category  # small 类

        self.name = ''  # 名称
        self.summary = ''  # 简介
        self.avatar_url = ''  # 头像

    @property
    def to_json(self):
        return self.__dict__
