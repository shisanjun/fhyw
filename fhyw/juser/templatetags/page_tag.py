# -*- coding:utf-8 -*-
__author__ = 'lixiang'
from django import template
from django.utils.html import format_html
register=template.Library()

@register.simple_tag
def page_curent_show(current_page,loop_page):
    """只显示3页码"""
    offset=abs(current_page-loop_page)
    if offset<3:
        if current_page==loop_page:
            #激活当前页
            page_ele='<li class="footable-page active"><a data-page="1" href="?page=%s">%s</a></li>' %(loop_page,loop_page)
        else:
            page_ele='<li class="footable-page"><a data-page="1" href="?page=%s">%s</a></li>' %(loop_page,loop_page)

        return format_html(page_ele)
    else:
        return ""


