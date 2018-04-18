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

class CpuPlugin(BasePlugin):
    """获取CPU信息"""
    def linux(self):
        """执行获取CPU命令"""
        response=BaseResponse()
        try:
            shell_cmd="cat /proc/cpuinfo"
            output=self.exec_shell_cmd(shell_cmd)
            response.data=self.parse(output)

        except Exception as e:

            msg="%s linux cpu plugin error:%s" %(self.host_ip,traceback.format_exc())
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
        response={"cpu_count":0,"cpu_physical_count":None,"cpu_model":None}
        cpu_physical_set=set()

        """
        processor	: 7
        model name	: Quad-Core AMD Opteron(tm) Processor 2378
        physical id	: 1
       """
        #subprocess output.stdout.read() or paramiko read() \n\n是大段分割，\n行分割
        for row in content.split("\n\n"):
            for item in row.split("\n"):
                sp=item.strip().split(":")
                if "processor" in item:
                    response["cpu_count"]+=1
                if "model name" in item:
                    response["cpu_model"]=sp[1]
                if "physical id" in item:
                    cpu_physical_set.add(sp[1])

        response["cpu_physical_count"]=len(cpu_physical_set)

        return response
