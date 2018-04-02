from django.conf.urls import url
from django.contrib import admin
from juser import views

urlpatterns = [
    url(r'login', views.login, name="login"),
    url(r'^index$', views.index, name="index"),
    url(r'logout$', views.logout, name="logout"),
    url(r'user$', views.user_list, name="user_list"),
    url(r'user_add$', views.user_add, name="user_add"),
    url(r'menu$', views.menu_list, name="menu_list"),
]
