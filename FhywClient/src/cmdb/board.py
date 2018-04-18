# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import sys
#traceback用来跟踪异常返回信息
import traceback
#获取父级父级的目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#加入系统环境
sys.path.append(BASE_DIR)

from src.cmdb.base import BasePlugin
from src.lib.response import BaseResponse

class BoardPlugin(BasePlugin):
    """获取主板信息"""
    def linux(self):
        """执行获取主板命令"""
        response=BaseResponse()
        try:
            shell_cmd="dmidecode -t system"
            output=self.exec_shell_cmd(shell_cmd)
            response.data=self.parse(output)
        except Exception as e:

            msg="%s linux main board plugin error:%s" %(self.host_ip,traceback.format_exc())
            self.logger.log(msg,mode=False)
            response.status=False
            response.error=msg
        return response

    @staticmethod
    def parse(content):
        """
        解析shell命令结果
        :param self:
        :param content:shell命令结果
        :return: 解析后的结果
        """

        response={}

        board_dict={
            "Manufacturer":"manufacturer", #服务器厂商
            "Product Name":"model", #服务器型号
            "Serial Number":"sn", #主板SN

        }

        #subprocess output.stdout.read() or paramiko read() \n\n是大段分割，\n行分割
        for row in content.split("\n\n"):
            for item in row.split("\n"):
                item=item.strip()
                try:
                    key,value=item.split(":")
                except:
                    key=item.split(":")[0]
                    value=""
                if key.strip() in board_dict:
                    response[board_dict[key.strip()]]=value.strip()

        return response

