# -*- coding:utf-8 -*-
__author__ = 'lixiang'

from django import forms
from django.forms import widgets
from juser import models
from django.core.exceptions import ValidationError


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
    seq = forms.IntegerField(error_messages={"required": "菜单位置序号为空"},
                             widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))
    comment = forms.CharField(required=False, widget=widgets.Textarea(attrs={"class": "form-control input-sm"}))


class Menu2Form(forms.Form):
    name = forms.CharField(
            error_messages={"required": "请输入菜单名"},
            widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))

    seq = forms.IntegerField(
            error_messages={"required": "请输入菜单位置序号"},
            widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))

    url_type = forms.ChoiceField(
            initial=0,
            choices=((0, "相对URL"),
                     (1, "绝对URL"),),
            error_messages={"required": "请选择URL类型"},
            widget=widgets.Select(attrs={"class": "form-control input-sm"}))

    url = forms.CharField(
            error_messages={"required": "请输入URL地址"},
            widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))

    menu_id = forms.ChoiceField(
            widget=widgets.Select(attrs={"class": "form-control input-sm"}))

    comment = forms.CharField(
            required=False,
            widget=widgets.Textarea(
                    attrs={"class": "form-control input-sm",
                           "rows": "5"}))

    def __init__(self, *args, **kwargs):
        super(Menu2Form, self).__init__(*args, **kwargs)
        self.fields["menu_id"].choices = models.Menu.objects.all().values_list("id", "name")

    def clean_name(self):
        menu_obj = models.Menu2.objects.filter(name=self.cleaned_data["name"]).first()
        if not menu_obj:
            return self.cleaned_data["name"]
        else:
            # 如果获取的ID和查询的ID一样表示原值，不需要抛异常，如果不一样表示修的名称和数据中其他名称有相同
            if self.initial.get("id") == menu_obj.id:
                return self.cleaned_data["name"]
            else:
                raise ValidationError("菜单名已存在", code="name")


class RoleForm(forms.Form):
    name = forms.CharField(
            error_messages={"required": "请输入角色名"},
            widget=widgets.TextInput(attrs={"class": "form-control input-sm"}))

    menu = forms.MultipleChoiceField(
            error_messages={"required": "请选择菜单权限"},
            widget=widgets.SelectMultiple(attrs={"class": "form-control input-sm"}))

    comment = forms.CharField(
            required=False,
            widget=widgets.Textarea(
                    attrs={"class": "form-control input-sm",
                           "rows": "5"}))

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields["menu"].choices = models.Menu.objects.all().values_list("id", "name")

    def clean_name(self):
        role_obj = models.Role.objects.filter(name=self.cleaned_data["name"]).first()
        if not role_obj:
            return self.cleaned_data["name"]
        else:
            # 如果获取的ID和查询的ID一样表示原值，不需要抛异常，如果不一样表示修的名称和数据中其他名称有相同
            if self.initial.get("id") == role_obj.id:
                return self.cleaned_data["name"]
            else:
                raise ValidationError("角色名已存在", code="name")
