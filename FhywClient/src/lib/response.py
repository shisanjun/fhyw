# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import json

class BaseResponse(object):
    def __init__(self):
        self.status=True
        self.message=None
        self.data=None
        self.error=None
