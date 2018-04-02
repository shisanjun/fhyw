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

    is_active = forms.BooleanField(
            initial=True,
            widget=widgets.CheckboxInput(attrs={"class": "magic-checkbox","id":"demo-form-checkbox"}))
    is_admin = forms.BooleanField(
            initial=False,
            widget=widgets.CheckboxInput(attrs={"class": "magic-checkbox"}))
