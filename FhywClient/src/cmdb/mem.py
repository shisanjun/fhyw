# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import sys
#traceback用来跟踪异常返回信息
import traceback
import copy
#获取父级父级的目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#加入系统环境
sys.path.append(BASE_DIR)

from src.cmdb.base import BasePlugin
from src.lib.response import BaseResponse
from src.lib.conver import mb2gb
class MemPlugin(BasePlugin):
    """获取mem信息"""
    def linux(self):
        """执行获取mem命令"""
        response=BaseResponse()
        try:
            shell_cmd="dmidecode -t  memory"
            output=self.exec_shell_cmd(shell_cmd)
            response.data=self.parse(output)

        except Exception as e:

            msg="%s linux mem plugin error:%s" %(self.host_ip,traceback.format_exc())
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
        reponse=[]

        mem_dict={
            "Size":"size", #大小
            "Locator":"locator", #内存位置
            "Type":"type", #内存类型
            "Speed":"speed",#内存速度
            "Manufacturer":"manufacturer",#内存厂商
            "Serial Number":"sn"#内存SN
        }
        """
        Size: 16384 MB
        Locator: DIMM_A1
        ....
        """

        #Memory Device来切割大段，\n\t行分割
        for item in content.split("Memory Device"):
            item=item.strip()
            mem_dict_tmp={}
            for row in item.split("\n\t"):
                try:
                    key,value=row.split(":")
                except:
                    key=row.split(":")[0]
                    value=""
                if key.strip() in mem_dict:

                    if key.strip()=="Size":
                        mem_dict_tmp["size"]=mb2gb(value.strip())

                    else:
                        mem_dict_tmp[mem_dict[key.strip()]]=value.strip()
            if len(mem_dict_tmp)!=0:
                reponse.append(copy.deepcopy(mem_dict_tmp))

        return reponse