# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import sys

#获取父级目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#加入系统环境
sys.path.append(BASE_DIR)


from src.cmdb.cmdb_plugin import CmdbPlugin

if __name__=="__main__":
    obj=CmdbPlugin()
    obj.post_asset()