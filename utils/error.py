#!/usr/bin/env python
# -*- coding: utf-8 -*-


class UrlsEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("The urls pool is empty")
