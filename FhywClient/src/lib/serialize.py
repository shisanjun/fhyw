# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import json as default_json
from json.encoder import JSONEncoder
from src.lib.response import BaseResponse


class JsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseResponse):
            return o.__dict__
        return JSONEncoder.default(self, o)


class Json(object):

    @staticmethod
    def dumps(response, ensure_ascii=True):
        return default_json.dumps(response, ensure_ascii=ensure_ascii, cls=JsonEncoder)