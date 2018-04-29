# _*_ coding:utf-8 _*_
__author__ = "lixiang"

import os
import sys
import copy

#traceback用来跟踪异常返回信息
import traceback

#获取父级父级的目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#加入系统环境
sys.path.append(BASE_DIR)

from src.cmdb.base import BasePlugin
from src.lib.response import BaseResponse
from src.lib.conver import mb2gb
class DiskPlugin(BasePlugin):
    """获取DISK信息"""
    def __init__(self,*args,**kwargs):
        super(DiskPlugin,self).__init__(*args,**kwargs)
        self.response=BaseResponse()

    def raid(self):
        """判断是否有RAID卡"""
        output=self.exec_shell_cmd("lspci |grep RAID")
        if len(output.strip())==0:
            return False
        else:
            #必有RAID卡

            return True

    def linux(self):
        """执行获取DISK命令"""

        try:
            if self.raid():
                self.response.data=self.has_raid_parse()
            else:
                self.response.data=self.not_has_raid_parse()

        except Exception as e:

            msg="%s linux Disk plugin error:%s" %(self.host_ip,traceback.format_exc())
            self.logger.log(msg,mode=False)
            self.response.status=False
            self.response.error=msg
        return self.response

    def has_raid_parse(self):
        """
        有RAID卡，通过MegaCli64获取raid卡里面硬盘信息
        :return:
        """
        self.get_disk_type()
        output=self.exec_shell_cmd("MegaCli64  -PDList -aALL")
        content=output.strip()

        response=[]
        disk_dict={}

        #subprocess output.stdout.read() or paramiko read() \n\n是大段分割，\n行分割
        for item in content.split("\n\n"):
            for row in item.split("\n"):
                row=row.strip()
                try:
                    key,val=row.split(":")
                except:
                    key=row.split(":")[0]
                    val=""
                key=key.strip()
                val=val.strip()
                if "Slot Number" in row:
                    disk_dict["slot"]=val
                if "PD Type" in row:
                    disk_dict["pd_type"]=val
                if "Raw Size" in row:
                    disk_dict["size"]=mb2gb(val)
                if "Inquiry Data" in row:
                    disk_dict["model"]=val
            if len(disk_dict)==0:
                continue

            response.append(copy.deepcopy(disk_dict))
        return response

    def not_has_raid_parse(self):
        """
        没有raid卡获取硬盘信息
        :return:
        """

        response=[]

        disk_type_list=self.get_disk_type()

        import operator
        #按照item中的第一个字符进行排序，即按KEY
        sorted_fdisk_list=sorted(self.get_fdisk().items(),key=operator.itemgetter(0))

        for i in range(min(len(disk_type_list),len(sorted_fdisk_list))):
            response_dict={}
            response_dict["slot"]=str(disk_type_list[i].get("id"))
            response_dict["pd_type"]="unknow"
            response_dict["size"]=str(sorted_fdisk_list[i][1])
            response_dict["model"]="%s %s" %(disk_type_list[i].get("vendeor"),disk_type_list[i].get("model"))
            response.append(copy.deepcopy(response_dict))

        return response


    def get_fdisk(self):
        """通过fdisk获取硬盘大小"""
        fdisk_output=self.exec_shell_cmd("fdisk -l")
        fdisk_list={}
        #以\n分割行
        for row in fdisk_output.split("\n"):
            row=row.strip()
            fdisk_dict={}
            if row.startswith("Disk") and not row.startswith("Disk identifier"):
                sp=row.split()
                #Disk /dev/sda: 599.6 GB, 599550590976 bytes
                fdisk_dict[sp[1].split(":")[0]]=sp[2]
                fdisk_list.update(copy.deepcopy(fdisk_dict))
        return fdisk_list

    def get_disk_type(self):
        """通过scsi获取硬盘厂商和型号"""

        #过滤DVD光驱，FC光纤存储，逻辑分区
        disk_type_not_need=["DVD-ROM","FC","Logical"]
        scsi_output=self.exec_shell_cmd("cat /proc/scsi/scsi")
        disk_list=[]
        count=0
        for row in scsi_output.split("\n"):
            row=row.strip()
            disk_dict={}
            if row.startswith("Vendor"):
                sp=row.split("Model:")
                #Vendor
                vendeor=str(sp[0].split(":")[1]).strip()
                #Model
                model=str(sp[1].split("Rev:")[0]).strip()

                #Vendor: DELL     Model: PERC H710        Rev: 3.13
                if model.split()[0] in disk_type_not_need:
                    continue
                else:
                    #硬盘中的顺应
                    disk_dict["id"]=count
                    disk_dict["vendeor"]=vendeor
                    disk_dict["model"]=model
                    disk_list.append(copy.deepcopy(disk_dict))
                    count+=1

        return disk_list
