# _*_ coding:utf-8 _*_
__author__ = "lixiang"
import json
from jasset import models

class DealResponseAsset(object):
    def __init__(self,request):
        self.request=request
        self.asset_record_list=[]
        self.error_log_list=[]
        try:
            self.data=json.loads(self.request.body)
        except:
            self.data={}

    def create_asset_record_obj(self,asset_id,content):
        """创建asset_record对象"""

        asset_obj=models.AssetRecord(asset_id=asset_id,content=content)

        self.asset_record_list.append(asset_obj)

    def create_error_log_obj(self,asset_id,title,content):
        """创建error_log对象"""
        error_obj=models.ErrorLog(asset_id=asset_id,title=title,content=content)
        self.error_log_list.append(error_obj)

    def create_bluck_record_and_error(self):
        """"批量创建asset_record和error_log记录"""
        try:
            models.AssetRecord.objects.bulk_create(self.asset_record_list)
            models.ErrorLog.objects.bulk_create(self.error_log_list)
        except Exception as e:
            print(e)

    def get_response_data(self,host_obj,type=None):
        """获取客户端反馈回的data数据"""
        error_info={
            "basic":"主机%s的系统信息收集运行程序basic报错，请检查" %host_obj.host_ip,
            "cpu":"主机%s的CPU运行程序cpu报错，请检查" %host_obj.host_ip,
            "board":"主机%s的主板运行程序board报错，请检查" %host_obj.host_ip,
            "mem":"主机%s的CPU运行程序mem报错，请检查" %host_obj.host_ip,
            "disk":"主机%s的CPU运行程序disk报错，请检查" %host_obj.host_ip,
        }
        try:
            response_dict=json.loads(self.data.get("data").get(type))
        except:
            return

        if not response_dict.get("status"):
            self.error_log_list(host_obj.asset.id,error_info[type],response_dict.get("error"))
            return

        data_dict=response_dict.get("data")

        if type not in ["mem","disk","nic"]:
            try:
                data_dict.update({"host_id":host_obj.id})
            except:
                print("host_obj no id")
                return

        return data_dict

    def deal_basic(self,host_obj):
        """系统基础信息"""
        basic_dict=self.get_response_data(host_obj,type="basic")
        if basic_dict is None:
            return

        basic_obj=models.HostBasic.objects.filter(host_id=host_obj.id).first()

        if not basic_obj:
            basic_obj=models.HostBasic.objects.create(**basic_dict)
            self.create_asset_record_obj(host_obj.asset_id,
                "[基础信息]新增提示： 资产：%s 主机IP：%s 主机名：%s 版本平台：%s 系统版本：%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                basic_obj.hostname,
                basic_obj.os_platform,
                basic_obj.os_version))

        else:
            if basic_obj.hostname!=basic_dict.get("hostname"):
                self.create_asset_record_obj(host_obj.asset_id,"[基础信息]更新提示：资产：%s 主机IP：%s 主机名由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                basic_obj.hostname,
                basic_dict.get("hostname")))
                basic_obj.hostname=basic_dict.get("hostname")

            if basic_obj.os_platform!=basic_dict.get("os_platform"):

                self.create_asset_record_obj(host_obj.asset_id,"[基础信息]更新提示：资产：%s 主机IP：%s 平台由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                basic_obj.os_platform,
                basic_dict.get("os_platform")))
                basic_obj.os_platform=basic_dict.get("os_platform")

            if basic_obj.os_version!=basic_dict.get("os_version"):

                self.create_asset_record_obj(host_obj.asset_id,"[基础信息]更新提示：资产：%s 主机IP：%s 系统版本由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                basic_obj.os_version,
                basic_dict.get("os_version"),))
                basic_obj.os_version=basic_dict.get("os_version")
            basic_obj.save()

    def deal_cpu(self,host_obj):
        """CPU信息处理"""
        cpu_dict=self.get_response_data(host_obj,type="cpu")
        if cpu_dict is None:
            return

        cpu_obj=models.HostCPU.objects.filter(host_id=host_obj.id).first()

        if not cpu_obj:
            cpu_obj=models.HostCPU.objects.create(**cpu_dict)
            self.create_asset_record_obj(host_obj.asset_id,
                "[CPU]新增提示： 资产：%s 主机IP：%s CPU个数：%s CPU物理个数：%s CPU型号：%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                cpu_obj.cpu_count,
                cpu_obj.cpu_physical_count,
                cpu_obj.cpu_model))

        else:
            if cpu_obj.cpu_count!=cpu_dict.get("cpu_count"):
                self.create_asset_record_obj(host_obj.asset_id,"[CPU]更新提示：资产：%s 主机IP：%s CPU个数：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                cpu_obj.cpu_count,
                cpu_dict.get("cpu_count")))
                cpu_obj.cpu_count=cpu_dict.get("cpu_count")

            if cpu_obj.cpu_physical_count!=cpu_dict.get("cpu_physical_count"):

                self.create_asset_record_obj(host_obj.asset_id,"[CPU]更新提示：资产：%s 主机IP：%s CPU物理个数：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                cpu_obj.cpu_physical_count,
                cpu_dict.get("cpu_physical_count")))
                cpu_obj.cpu_physical_count=cpu_dict.get("cpu_physical_count")

            if cpu_obj.cpu_model!=cpu_dict.get("cpu_model"):

                self.create_asset_record_obj(host_obj.asset_id,"[CPU]更新提示：资产：%s 主机IP：%s CPU型号：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                cpu_obj.cpu_model,
                cpu_dict.get("cpu_model"),))
                cpu_obj.cpu_model=cpu_dict.get("cpu_model")
            cpu_obj.save()

    def deal_board(self,host_obj):
        """主板信息处理"""
        board_dict=self.get_response_data(host_obj,type="board")
        if board_dict is None:
            return

        board_obj=models.HostBoard.objects.filter(host_id=host_obj.id).first()

        if not board_obj:
            board_obj=models.HostBoard.objects.create(**board_dict)
            self.create_asset_record_obj(host_obj.asset_id,
                "[主板]新增提示： 资产：%s 主机IP：%s 制造商：%s 型号：%s SN号：%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                board_obj.manufacturer,
                board_obj.model,
                board_obj.sn))

        else:
            if board_obj.manufacturer!=board_dict.get("manufacturer"):
                self.create_asset_record_obj(host_obj.asset_id,"[主板]更新提示：资产：%s 主机IP：%s 制造商：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                board_obj.manufacturer,
                board_dict.get("manufacturer")))
                board_obj.manufacturer=board_dict.get("manufacturer")

            if board_obj.model!=board_dict.get("model"):

                self.create_asset_record_obj(host_obj.asset_id,"[主板]更新提示：资产：%s 主机IP：%s 主板型号：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                board_obj.model,
                board_dict.get("model")))
                board_obj.model=board_dict.get("model")

            if board_obj.sn!=board_dict.get("sn"):

                self.create_asset_record_obj(host_obj.asset_id,"[主板]更新提示：资产：%s 主机IP：%s 主板SN：由%s更新为%s" %(
                host_obj.asset.device_type.name,
                host_obj.host_ip,
                board_obj.sn,
                board_dict.get("sn"),))
                board_obj.sn=board_dict.get("sn")
            board_obj.save()

    def deal_memory(self,host_obj):
        """内存信息处理"""

        #返回的是字典列表
        memory_list=self.get_response_data(host_obj,type="mem")
        if memory_list is None:
            return

        #用来存放内存的插槽位，用来与数据库中相应主机下的内存做比较，与之少了，说明内存出故障
        response_mem_list=[]

        #memory_dict ={'speed': '1333 MHz', 'locator': 'DIMM_G1', 'sn': '148160F7', 'size': '8', 'type': 'DDR3', 'manufacturer': 'Samsung'}
        for memory_dict in memory_list:

            response_mem_list.append(memory_dict.get("locator"))

            try:
                memory_dict.update({"host_id":host_obj.id})
            except:
                print("host_obj no id")
                return

            mem_obj=models.HostMemory.objects.filter(host_id=host_obj.id,locator=memory_dict.get("locator")).first()

            if not mem_obj:
                mem_obj=models.HostMemory.objects.create(**memory_dict)
                self.create_asset_record_obj(host_obj.asset_id,
                    "[内存]新增提示： 资产：%s 主机IP：%s 插槽位：%s 制造商：%s 型号：%s 大小(GB)：%s 内存SN号：%s 速度：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.manufacturer,
                    mem_obj.type,
                    mem_obj.size,
                    mem_obj.sn,
                    mem_obj.speed))

            else:
                if mem_obj.locator!=memory_dict.get("locator"):
                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 插槽位：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.locator,
                    memory_dict.get("locator")))
                    mem_obj.locator=memory_dict.get("locator")

                if mem_obj.manufacturer!=memory_dict.get("manufacturer"):
                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 制造商：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.manufacturer,
                    memory_dict.get("manufacturer")))
                    mem_obj.manufacturer=memory_dict.get("manufacturer")

                if mem_obj.type!=memory_dict.get("type"):
                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 型号：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.type,
                    memory_dict.get("type")))
                    mem_obj.type=memory_dict.get("type")


                if mem_obj.size!=memory_dict.get("size"):

                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 大小(GB)：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.size,
                    memory_dict.get("size")))
                    mem_obj.size=memory_dict.get("size")

                if mem_obj.sn!=memory_dict.get("sn"):

                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 内存SN号：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.sn,
                    memory_dict.get("sn"),))
                    mem_obj.sn=memory_dict.get("sn")

                if mem_obj.speed!=memory_dict.get("speed"):

                    self.create_asset_record_obj(host_obj.asset_id,"[内存]更新提示：资产：%s 主机IP：%s 槽位标识：%s 速度：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_obj.locator,
                    mem_obj.speed,
                    memory_dict.get("speed")))
                    mem_obj.speed=memory_dict.get("speed")
                mem_obj.save()

        #处理内存条是不是缺少
        mem_update_before_list= [x[0] for x in list(models.HostMemory.objects.filter(host_id=host_obj.id).values_list("locator"))]
        less_mem_list=set(mem_update_before_list)-set(response_mem_list)
        if len(less_mem_list)!=0:
            for item in less_mem_list:
                mem_del_obj=models.HostMemory.objects.filter(host_id=host_obj.id,locator=item).first()

                self.create_asset_record_obj(host_obj.asset_id,
                    "[内存]删除提示： 资产：%s 主机IP：%s 插槽位：%s 制造商：%s 型号：%s 大小(GB)：%s 内存SN号：%s 速度：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    mem_del_obj.locator,
                    mem_del_obj.manufacturer,
                    mem_del_obj.type,
                    mem_del_obj.size,
                    mem_del_obj.sn,
                    mem_del_obj.speed))
                self.create_error_log_obj(host_obj.asset_id,"主机IP：%s [内存]丢失报警" %host_obj.host_ip,
                    "[内存]丢失提示：插槽位：%s 制造商：%s 型号：%s 大小(GB)：%s 内存SN号：%s 速度：%s" %(
                    mem_del_obj.locator,
                    mem_del_obj.manufacturer,
                    mem_del_obj.type,
                    mem_del_obj.size,
                    mem_del_obj.sn,
                    mem_del_obj.speed))
                mem_del_obj.delete()

    def deal_disk(self,host_obj):
        """硬盘信息处理"""
        #返回的是字典列表
        disk_list=self.get_response_data(host_obj,type="disk")
        if disk_list is None:
            return

        #用来存放硬盘的插槽位，用来与数据库中相应主机下的硬盘做比较，与之少了，说明内存出故障
        response_disk_list=[]

        for disk_dict in disk_list:
            response_disk_list.append("%s" %disk_dict.get("slot"))

            try:
                disk_dict.update({"host_id":host_obj.id})
            except:
                print("host_obj no id")
                return

            disk_obj=models.HostDisk.objects.filter(host_id=host_obj.id,slot=disk_dict.get("slot")).first()

            if not disk_obj:
                disk_obj=models.HostDisk.objects.create(**disk_dict)
                self.create_asset_record_obj(host_obj.asset_id,
                    "[硬盘]新增提示： 资产：%s 主机IP：%s 插槽位：%s 磁盘厂商(型号)：%s 磁盘容量GB：%s 磁盘类型：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_obj.slot,
                    disk_obj.model,
                    disk_obj.size,
                    disk_obj.pd_type,))

            else:
                if str(disk_obj.slot)!=str(disk_dict.get("slot")):
                    self.create_asset_record_obj(host_obj.asset_id,"[硬盘]更新提示：资产：%s 主机IP：%s 槽位标识：%s 插槽位：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_obj.slot,
                    disk_obj.slot,
                    disk_dict.get("slot")))
                    disk_obj.slot=disk_dict.get("slot")

                if disk_obj.model!=disk_dict.get("model"):
                    self.create_asset_record_obj(host_obj.asset_id,"[硬盘]更新提示：资产：%s 主机IP：%s 槽位标识：%s 磁盘厂商(型号)：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_obj.slot,
                    disk_obj.model,
                    disk_dict.get("model")))
                    disk_obj.model=disk_dict.get("model")

                if str(disk_obj.size)!=str(disk_dict.get("size")):

                    self.create_asset_record_obj(host_obj.asset_id,"[硬盘]更新提示：资产：%s 主机IP：%s 槽位标识：%s 磁盘容量GB：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_obj.slot,
                    disk_obj.size,
                    disk_dict.get("size")))
                    disk_obj.size=disk_dict.get("size")

                if disk_obj.pd_type!=disk_dict.get("pd_type"):

                    self.create_asset_record_obj(host_obj.asset_id,"[硬盘]更新提示：资产：%s 主机IP：%s 槽位标识：%s 磁盘类型：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_obj.slot,
                    disk_obj.pd_type,
                    disk_dict.get("pd_type"),))
                    disk_obj.pd_type=disk_dict.get("pd_type")

                disk_obj.save()



        #获取相应主机下的所有硬盘插槽位
        disk_update_before_list=[x[0] for x in list(models.HostDisk.objects.filter(host_id=host_obj.id).values_list("slot"))]

        #处理硬盘是不是缺少
        less_disk_list=set(disk_update_before_list)-set(response_disk_list)
        if len(less_disk_list)!=0:
            for item in less_disk_list:
                disk_del_obj=models.HostDisk.objects.filter(host_id=host_obj.id,slot=item).first()

                self.create_asset_record_obj(host_obj.asset_id,
                    "[硬盘]删除提示： 资产：%s 主机IP：%s 插槽位：%s 磁盘厂商(型号)：%s 磁盘容量GB：%s 磁盘类型：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    disk_del_obj.slot,
                    disk_del_obj.model,
                    disk_del_obj.size,
                    disk_del_obj.pd_type,))

                self.create_error_log_obj(host_obj.asset_id,"主机IP：%s [硬盘]丢失报警" %host_obj.host_ip,
                    "[硬盘]删除提示： 插槽位：%s 磁盘厂商(型号)：%s 磁盘容量GB：%s 磁盘类型：%s" %(
                    disk_del_obj.slot,
                    disk_del_obj.model,
                    disk_del_obj.size,
                    disk_del_obj.pd_type,))
                disk_del_obj.delete()

    def deal_nic(self,host_obj):
        """网卡信息处理"""
        nic_dicts=self.get_response_data(host_obj,type="nic")
        if nic_dicts is None:
            return

        #用来存放网卡名称，用来与数据库中相应主机下的网卡做比较，与之少了，说明网卡出故障
        response_nic_list=[]
        for nic_name,nic_dict in nic_dicts.items():
            response_nic_list.append(nic_name)

            try:
                nic_dict.update({"name":nic_name})
                nic_dict.update({"host_id":host_obj.id})
            except:
                print("host_obj no id")
                return

            nic_obj=models.HostNIC.objects.filter(host_id=host_obj.id,name=nic_dict.get("name")).first()

            if not nic_obj:
                nic_obj=models.HostNIC.objects.create(**nic_dict)
                self.create_asset_record_obj(host_obj.asset_id,
                    "[网卡]新增提示： 资产：%s 主机IP：%s 网卡名称：%s 网卡mac地址：%s 子网掩码：%s ip地址：%s 网卡状态：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_obj.name,
                    nic_obj.hwaddr,
                    nic_obj.netmask,
                    nic_obj.ipaddrs,
                    nic_obj.up))

            else:
                if nic_obj.hwaddr!=str(nic_dict.get("hwaddr")):
                    self.create_asset_record_obj(host_obj.asset_id,"[网卡]更新提示：资产：%s 主机IP：%s 网卡名称：%s 网卡mac地址：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_obj.name,
                    nic_obj.hwaddr,
                    nic_dict.get("hwaddr")))
                    nic_obj.hwaddr=nic_dict.get("hwaddr")

                if nic_obj.netmask!=nic_dict.get("netmask"):
                    self.create_asset_record_obj(host_obj.asset_id,"[网卡]更新提示：资产：%s 主机IP：%s 网卡名称：%s 子网掩码(型号)：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_obj.name,
                    nic_obj.netmask,
                    nic_dict.get("netmask")))
                    nic_obj.netmask=nic_dict.get("netmask")

                if nic_obj.ipaddrs!=str(nic_dict.get("ipaddrs")):

                    self.create_asset_record_obj(host_obj.asset_id,"[网卡]更新提示：资产：%s 主机IP：%s 网卡名称：%s ip地址：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_obj.name,
                    nic_obj.ipaddrs,
                    nic_dict.get("ipaddrs")))
                    nic_obj.ipaddrs=nic_dict.get("ipaddrs")

                if nic_obj.up!=nic_dict.get("up"):

                    self.create_asset_record_obj(host_obj.asset_id,"[硬盘]更新提示：资产：%s 主机IP：%s 网卡名称：%s 网卡状态：由%s更新为%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_obj.name,
                    nic_obj.up,
                    nic_dict.get("up"),))
                    nic_obj.up=nic_dict.get("up")
                nic_obj.save()

        #获取主机下的所有网卡名称
        nic_update_before_list=[x[0] for x in list(models.HostNIC.objects.filter(host_id=host_obj.id).values_list("name"))]
        #处理网卡是不是缺少
        less_nic_list=set(nic_update_before_list)-set(response_nic_list)
        if len(less_nic_list)!=0:
            for item in less_nic_list:
                nic_del_obj=models.HostNIC.objects.filter(host_id=host_obj.id,name=item).first()

                self.create_asset_record_obj(host_obj.asset_id,
                    "[网卡]删除提示： 资产：%s 主机IP：%s 网卡名称：%s 网卡mac地址：%s 子网掩码：%s ip地址：%s 网卡状态：%s" %(
                    host_obj.asset.device_type.name,
                    host_obj.host_ip,
                    nic_del_obj.name,
                    nic_del_obj.hwaddr,
                    nic_del_obj.netmask,
                    nic_del_obj.ipaddrs,
                    nic_del_obj.up))

                self.create_error_log_obj(host_obj.asset_id,"主机IP：%s [网卡]丢失报警" %host_obj.host_ip,
                    "[网卡]删除提示：网卡名称：%s 网卡mac地址：%s 子网掩码：%s ip地址：%s 网卡状态：%s" %(
                    nic_del_obj.name,
                    nic_del_obj.hwaddr,
                    nic_del_obj.netmask,
                    nic_del_obj.ipaddrs,
                    nic_del_obj.up))
                nic_del_obj.delete()

    def execute(self):

        host_obj=models.Host.objects.filter(host_ip=self.data.get("host")).first()
        if not host_obj:
            print("资产里面没有信息")
            return
        self.deal_basic(host_obj)
        self.deal_cpu(host_obj)
        self.deal_board(host_obj)
        self.deal_memory(host_obj)
        self.deal_disk(host_obj)
        self.deal_nic(host_obj)
        #批量创建asset_record和error_log记录
        self.create_bluck_record_and_error()



