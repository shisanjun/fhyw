from django.db import models
from juser.models import UserProfile

# Create your models here.
class IDC(models.Model):
    """机房信息"""
    name = models.CharField(max_length=64, verbose_name="机房名称")
    floor = models.CharField(max_length=64, verbose_name="楼层")

    def __str__(self):
        return "%s%s" % (self.name, self.floor)

    class Meta:
        db_table = "idc"
        unique_together = ("name", "floor")
        verbose_name = "机房信息"
        verbose_name_plural = "机房信息"


class DeviceType(models.Model):
    """设备类型"""
    name = models.CharField(max_length=64, unique=True, verbose_name="设备类型名称")
    comment = models.TextField(verbose_name="备注", null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        db_table = "devicetype"
        verbose_name = "设备类型"
        verbose_name_plural = "设备类型"


class Asset(models.Model):
    """资产信息"""
    device_type = models.ForeignKey("DeviceType", verbose_name="设备类型")
    device_status_choices = (
        (1, "上架"),
        (2, "在线"),
        (3, "离线"),
        (4, "下架"),
        (5, "报废"),
    )
    device_status = models.PositiveSmallIntegerField(choices=device_status_choices, default=2, verbose_name="设备状态")
    cabinet_num = models.CharField(max_length=64, verbose_name="机柜编号")
    cabinet_order = models.CharField(max_length=64, verbose_name="设备位置", help_text="设备在机柜中的位置，从下往上")
    idc = models.ForeignKey("IDC", verbose_name="机房位置")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "设备%s-机柜%s-位置%s" % (self.device_type, self.cabinet_num, self.cabinet_order)

    class Meta:
        db_table = "asset"
        verbose_name = "资产信息"
        verbose_name_plural = "资产信息"


class HostGroup(models.Model):
    """主机组"""

    name = models.CharField(max_length=64, unique=True, verbose_name="主机组")
    comment = models.TextField(verbose_name="备注",blank=True,null=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        db_table = "hostgroup"
        verbose_name = "主机组"
        verbose_name_plural = "主机组"


class Host(models.Model):
    """主机"""
    asset= models.OneToOneField('Asset',related_name="host",related_query_name="host" ,verbose_name="关联资产",null=True)
    hostgroup=models.ForeignKey("HostGroup",verbose_name="所属主机组",blank=True,null=True,related_query_name="host",related_name="host")
    host_ip = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.host_ip

    class Meta:
        db_table = "host"
        verbose_name_plural = "服务器表"


class HostBasic(models.Model):
    host = models.OneToOneField("Host", verbose_name="所属主机", related_name="basic",on_delete=models.CASCADE)
    hostname = models.CharField(max_length=128,blank=True,null=True)
    os_platform = models.CharField('系统', max_length=64, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.os_version

    class Meta:
        db_table = "hostbasic"
        verbose_name_plural = "基础信息表"


class HostBoard(models.Model):
    """主机主板信息"""
    host = models.OneToOneField("Host", verbose_name="所属主机",related_name="board",on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "%s%s" % (self.manufacturer, self.model)

    class Meta:
        db_table = "hostbord"
        verbose_name_plural = "主板表"


class HostCPU(models.Model):
    """主机CPU信息"""
    host = models.OneToOneField("Host", verbose_name="所属主机",related_name="cpu",on_delete=models.CASCADE)
    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "%s" % (self.cpu_model)

    class Meta:
        db_table = "hostcpu"
        verbose_name_plural = "CPU表"


class HostDisk(models.Model):
    """主机硬盘信息"""
    host = models.ForeignKey("Host", verbose_name="所属主机",related_name="disk",on_delete=models.CASCADE)
    slot = models.CharField('插槽位', max_length=8, null=True, blank=True)
    model = models.CharField('磁盘厂商(型号)', max_length=32, null=True, blank=True)
    size = models.FloatField('磁盘容量GB', null=True, blank=True)
    pd_type = models.CharField('磁盘类型', max_length=32, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.slot

    class Meta:
        db_table = "hostdisk"
        verbose_name_plural = "硬盘表"


class HostNIC(models.Model):
    """网卡信息"""
    host = models.ForeignKey('Host', verbose_name="所属主机",related_name="nic",on_delete=models.CASCADE)
    name = models.CharField(verbose_name='网卡名称', max_length=128)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=128, null=True, blank=True)
    netmask = models.CharField(max_length=64, verbose_name="子网掩码",null=True, blank=True)
    ipaddrs = models.CharField('ip地址', max_length=256, null=True, blank=True)
    up = models.BooleanField(verbose_name="网卡状态",default=False)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hostnic"
        verbose_name_plural = "网卡表"


class HostMemory(models.Model):
    """内存信息"""
    host = models.ForeignKey('Host', verbose_name="所属主机",related_name="memory",on_delete=models.CASCADE)
    locator = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    type = models.CharField('型号', max_length=64, null=True, blank=True)
    size = models.CharField(max_length=64,verbose_name='大小', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.locator

    class Meta:
        db_table = "hostmemory"
        verbose_name_plural = "内存表"

class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset = models.ForeignKey('Asset',related_query_name="assetrecord",related_name="assetrecord")
    content = models.TextField(null=True)
    creator = models.ForeignKey(UserProfile, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "资产记录表"
        db_table = "assetrecord"

    def __str__(self):
        return "%s-%s-%s" % (self.asset.idc.name, self.asset.cabinet_num, self.asset.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset= models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"
        db_table = "errorlog"
    def __str__(self):
        return self.title