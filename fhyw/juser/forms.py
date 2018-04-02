# -*- coding:utf-8 -*-
__author__ = 'lixiang'

from django import forms
from django.forms import widgets


class UserProfileForm(forms.Form):
    name = forms.CharField(max_length=64,
                           error_messages={"required": "用户名为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control input-sm"})
                           )
    email = forms.EmailField(
            error_messages={
                "required": "用户名为空",
                "invalid": "邮箱格式不正确"},
            widget=widgets.TextInput(attrs={"class": "form-control input-sm"})
    )
    password = forms.CharField(max_length=128,
                               widget=widgets.PasswordInput(attrs={"class": "form-control input-sm"}))

    is_active = forms.BooleanField()
    is_admin = forms.BooleanField()


class MenuForm(forms.Form):
    name = forms.CharField(error_messages={"required": "菜单名为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))
    seq = forms.IntegerField(error_messages={"required": "序号为空"},
                             widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))
    comment = forms.CharField(required=False,widget=widgets.Textarea(attrs={"class": "form-control input-sm"}))
