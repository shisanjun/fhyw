# -*- coding:utf-8 -*-
__author__ = 'lixiang'

import urllib3
import traceback
import json
from src.lib.log import Logger
class RequestHttp(object):
    _instance=None
    http=urllib3.PoolManager(timeout=10)
    logger=Logger()

    def __new__(cls, *args, **kwargs):
        """单例模式只返回一个实例"""
        if not cls.__instance:
            cls.__instance=object.__new__(cls,*args,**kwargs)
        return cls.__instance

    @classmethod
    def get_request(self,url=None):
        try:
            response=self.http.request(method="GET",url=url)
        except Exception as e:
            response="connect raise %s" %traceback.print_exc()

        return response

    @classmethod
    def post_request(self,url=None,msg=None):

        """
        发送数据
        :param url:发送的URL
        :param msg:字典形式
        :return:
        """
        try:
            #传入数据加编码
            encode_data=json.dumps(msg).encode("utf-8")

            #以json形式传递
            response=self.http.request(method="POST",url=url,body=encode_data,
                                  headers={"Content-Type":"application/json" })
            if response.status==200:
                self.logger.log(message="send data to %s success" %url,mode=True)
        # except ConnectionRefusedError as e:
        #     response="目标计算机积极拒绝，无法连接"

        except Exception as e:
            response="connect exception %s" %traceback.print_exc()

        return response


