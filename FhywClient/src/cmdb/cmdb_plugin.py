# -*- coding:utf-8 -*-
__author__ = 'lixiang'
import os, sys

# 获取父级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 加入系统环境
sys.path.append(BASE_DIR)

from src.cmdb.basic import BasicPlugin
from src.cmdb.board import BoardPlugin
from src.cmdb.cpu import CpuPlugin
from src.cmdb.disk import DiskPlugin
from src.cmdb.mem import MemPlugin
from src.cmdb.nic import NicPlugin
from src.lib.log import Logger
from src.lib.request import RequestHttp
from conf import settings
from src.lib.serialize import Json


class CmdbPlugin(object):
    """
    生成资产记录，并发送服务器
    """

    def __init__(self):
        self.response_info = {}
        self.response_info["host"] = settings.LOCAL_IP
        self.response_info["data"] = {}
        self.logger = Logger()
        self.asset_url="http://%s:%s/%s" %(settings.servier["Host"],settings.servier["Port"],settings.cmdb["cmdb_report"])

        self.make_asset()

    def make_asset(self):
        """
        生成数据报表
        :return:
        """
        report_dict = {
            "basic": BasicPlugin,
            "board": BoardPlugin,
            "cpu": CpuPlugin,
            "disk": DiskPlugin,
            "mem": MemPlugin,
            'nic':NicPlugin,
        }

        for key, value in report_dict.items():
            report_obj = value()
            report_response = report_obj.execute()
            #BaseResponse序列化成字典
            self.response_info["data"][key] = Json.dumps(report_response)


    def post_asset(self):
        """
        发送数据
        :return:
        """
        RequestHttp.post_request(url=self.asset_url, msg=self.response_info)
