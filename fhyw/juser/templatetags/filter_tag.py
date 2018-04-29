# -*- coding:utf-8 -*-
__author__ = 'lixiang'
from django import template
from django.utils.html import format_html
from django.utils.html import mark_safe
from django.urls import reverse

register = template.Library()


@register.simple_tag
def page_curent_show(current_page, loop_page):
    """只显示3页码"""
    offset = abs(current_page - loop_page)
    if offset < 3:
        if current_page == loop_page:
            # 激活当前页
            page_ele = '<li class="footable-page active"><a data-page="1" href="?page=%s">%s</a></li>' % (
                loop_page, loop_page)
        else:
            page_ele = '<li class="footable-page"><a data-page="1" href="?page=%s">%s</a></li>' % (loop_page, loop_page)

        return format_html(page_ele)
    else:
        return ""


@register.simple_tag
def show_menus(request):
    """
    菜单功能显示
    """
    menu_list = []
    for role in request.user.role.all():
        for menu in role.menu.all():
            if menu not in menu_list:
                menu_list.append(menu)
    menu_one_str = ""
    for index, menu in enumerate(menu_list):
        if index==0:
            menu_one_str += """
               <li class="active-sub">
                    <a href="#"><i class="ti-wallet"></i>
                    <span class="menu-title">{menu}</span>
                    <i class="arrow"></i>
                    </a>
                    <ul class="collapse in">""".format(menu=menu.name)
        else:
            menu_one_str += """
               <li class="active-sub">
                    <a href="#"><i class="ti-wallet"></i>
                    <span class="menu-title">{menu}</span>
                    <i class="arrow"></i>
                    </a>
                    <ul class="collapse in">""".format(menu=menu.name)

        for menu2 in menu.menu2_set.all().order_by("seq"):

            if menu2.url_type == 0:
                try:
                    menu_one_str += '<li class="active-link"><a href="' + reverse(
                        menu2.url) + '">' + menu2.name + '</a></li>'
                except:
                    menu_one_str += '<li class="active-link"><a href="">' + menu2.name + '</a></li>'
            else:
                menu_one_str += '<li class="active-link"><a href="' + menu2.url + '">' + menu2.name + '</a></li>'

        menu_one_str += " </ul></li>"
    return mark_safe(menu_one_str)
