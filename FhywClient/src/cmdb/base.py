# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import os
import sys

#获取父级目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#加入系统环境
sys.path.append(BASE_DIR)

from conf import settings
from src.lib.log import Logger

class BasePlugin(object):
    def __init__(self):
        self.model=settings.MODE
        self.logger=Logger()
        self.host_ip=settings.LOCAL_IP

    def agent(self,cmd):
        import subprocess
        output=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return output.stdout.read().decode("utf-8")
    #
    # def ssh(self,cmd):
    #     import paramiko
    #     private_key=paramiko.RSAKey

    def exec_shell_cmd(self,cmd):
        """根据接口不同，执行相应的命令"""
        if getattr(self,self.model):
            func=getattr(self,self.model)
            output=func(cmd)
        else:
            output=self.agent(cmd)
        return output

    def execute(self):
        return self.linux()

    def linux(self):
        raise Exception("You mush implement linux method")
