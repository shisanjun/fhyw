# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import sys
# traceback用来跟踪异常返回信息
import traceback

# 获取父级父级的目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 加入系统环境
sys.path.append(BASE_DIR)

from src.cmdb.base import BasePlugin
from src.lib.response import BaseResponse


class BasicPlugin(BasePlugin):
    """获取平台，版本，主机名"""

    def os_platform(self):
        """获取平台名称"""
        output = self.exec_shell_cmd("uname")
        #output.strip()j
        return output.strip()

    def os_version(self):
        """获取系统名称"""
        output = self.exec_shell_cmd("cat /etc/redhat-release")
        return output.strip()

    def hostname(self):
        """获取系统主机名"""
        output = self.exec_shell_cmd("hostname")
        return output.strip()

    def linux(self):
        """执行获取平台，版本，主机名命令"""
        response = BaseResponse()
        try:
            response.data = {
                "os_platform": self.os_platform(),
                "os_version": self.os_version(),
                "hostname": self.hostname(),
            }
        except Exception as e:

            msg = "%s linux basic plugin error:%s" % (self.host_ip, traceback.format_exc())
            self.logger.log(msg, mode=False)
            response.status = False
            response.error = msg
        return response
