# _*_ coding:utf-8 _*_
__author__ = "lixiang"
from django import template
import copy
from django.utils.html import mark_safe
register=template.Library()

@register.simple_tag
def dsik_summary_info(host_obj):
    """显示硬盘汇总信息"""
    disk_size_count=0
    index=-1
    try:
        for index,disk_obj in enumerate(host_obj.disk.all()):
            disk_size_count+=disk_obj.size

        response="%s块硬盘 硬盘总空间大小为：%sG" %(index+1,str(round(disk_size_count,2)))
    except:
        response=""

    return response

@register.simple_tag
def dsik_sum_size(host_obj):
    """显示硬盘总大小"""
    disk_size_count=0

    try:
        for index,disk_obj in enumerate(host_obj.disk.all()):
            disk_size_count+=disk_obj.size

        disk_size_count=str(int(disk_size_count))
    except:
        disk_size_count=""

    if disk_size_count==0:
        disk_size_count=""

    return disk_size_count

@register.simple_tag
def mem_summary_info(host_obj):
    """显示内存汇总信息"""
    mem_size_count=0
    use_count=0
    index=-1
    try:
        for index,mem_obj in enumerate(host_obj.memory.all()):
            if str(mem_obj.size).isdigit():
                mem_size_count+=int(mem_obj.size)
                use_count+=1

        response="%s个内存插槽 已使用%s个插槽 还剩余%s个插槽 内存总大小为：%sGB" %(index+1,str(use_count),str(index+1-use_count),str(round(mem_size_count,2)))
    except:
        response=""

    return response

@register.simple_tag
def mem_sum_sizes(host_obj):
    """显示内存汇总信息"""
    mem_size_count=0
    try:
        for index,mem_obj in enumerate(host_obj.memory.all()):
            if str(mem_obj.size).isdigit():
                mem_size_count+=int(mem_obj.size)
        mem_size_count=str(int(mem_size_count))
    except:
        mem_size_count=""

    if mem_size_count==0:
        mem_size_count=""

    return int(mem_size_count)


@register.simple_tag
def host_stat(hostgroup_objs):
    hostgroup_list=[]
    for hostgroup in hostgroup_objs:
        hostgroup_dict={
            "name":hostgroup.name,
            "value":hostgroup.host.all().count()
        }

        hostgroup_list.append(copy.deepcopy(hostgroup_dict))

    return mark_safe(hostgroup_list)


@register.simple_tag
def group_show_name(hostgroup_objs):

    hostgroup_name_list=[]
    for hostgroup in hostgroup_objs:
        hostgroup_name_list.append(hostgroup.name)

    print(type(mark_safe(hostgroup_name_list)))
    return mark_safe(hostgroup_name_list)