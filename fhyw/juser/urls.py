from django.conf.urls import url
from django.contrib import admin
from juser import views

urlpatterns = [

    url(r'user$', views.user_list, name="user_list"),
    url(r'user_add$', views.user_add, name="user_add"),

    url(r'menu$', views.menu_list, name="menu_list"),
    url(r'menu_add$', views.menu_add, name="menu_add"),
    url(r'menu_edit$', views.menu_edit, name="menu_edit"),
    url(r'menu_del$', views.menu_del, name="menu_del"),

    url(r'menu2$', views.menu2_list, name="menu2_list"),
    url(r'menu2_add$', views.menu2_add, name="menu2_add"),
    url(r'menu2_del$', views.menu2_del, name="menu2_del"),
    url(r'menu2_edit/(?P<id>\d+).html$', views.menu2_edit, name="menu2_edit"),

    url(r'role$', views.role_list, name="role_list"),
    url(r'role_add$', views.role_add, name="role_add"),
    url(r'role_del$', views.role_del, name="role_del"),
    url(r'role_edit/(?P<id>\d+).html$', views.role_edit, name="role_edit"),
]
