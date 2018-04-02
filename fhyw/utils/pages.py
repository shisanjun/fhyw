# -*- coding:utf-8 -*-
__author__ = 'lixiang'

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page(request,post_objects,page_number=20):
    """
    实现分页
    :param request:  view中request
    :param post_objects: 需要实现分页的对象（列表，queryset）
    :param page_number: #每页显示条数，默认20页
    :return:
    """
    #实例化结果集，    queryset转列表
    post_objects=list(post_objects)
    paginator = Paginator(post_objects, page_number) # Show 20 contacts per page

    #获取htmml中传递page值
    page = request.GET.get('page',1)
    try:
        #需要返回的值
        page_objs = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，返回第1页
        page_objs = paginator.page(1)
    except EmptyPage:
        # 如果page超出最大值 ，只显示最后一页
        page_objs = paginator.page(paginator.num_pages)

    return page_objs
