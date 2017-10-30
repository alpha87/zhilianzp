#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from zhilianzp.settings import HOST, PORT, PASSWORD
from .error import UrlsEmptyError


class RedisClient(object):

    def __init__(self):
        if PASSWORD:
            self._db = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
        else:
            self._db = redis.Redis(host=HOST, port=PORT)

    def get(self, count=1):
        """
        从redis中获取url
        """
        urls = self._db.lrange("urls", 0, count - 1)
        self._db.ltrim("urls", count, -1)
        return urls

    def put(self, url):
        """
        添加url到最右侧
        """
        self._db.rpush("urls", url)

    def pop(self):
        """
        从右侧取出url
        """
        try:
            return self._db.rpop("urls").decode("utf-8")
        except BaseException:
            raise UrlsEmptyError

    @property
    def queue_len(self):
        """
        得到整个队列的长度
        """
        return self._db.llen("urls")

    def flush(self):
        """
        刷新数据库
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
