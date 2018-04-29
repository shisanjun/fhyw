from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout,login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from juser import models
from jasset import models as asset_model
from utils.pages import page
from juser import forms
import json
import copy


# Create your views here.
@login_required
def index(request):
    hostgroup_objs=asset_model.HostGroup.objects.select_related()
    return render(request, "index.html",locals())


def acc_login(request):
    ret={"status":True,"error":None}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request,user)
            return redirect(reverse("index"))
        else:
            ret["status"]=False
            ret["error"]="用户名或者密码不正确"

    return render(request, "login.html",{"ret":ret})


def acc_logout(request):
    logout(request)
    return redirect(reverse("login"))


@login_required
def user_list(request):
    user_objs = models.UserProfile.objects.all()
    page_objs = page(request, user_objs)
    return render(request, "juser/user_list.html", {"page_objs": page_objs})

@login_required
def user_add(request):
    if request.method == "GET":
        user_form_obj = forms.UserProfileForm()

    elif request.method == "POST":
        user_form_obj = forms.UserProfileForm(request.POST)

    return render(request, "juser/user_add.html", {"user_form_obj": user_form_obj})

@login_required
def menu_list(request):
    """菜单列表"""
    ret = {"status": True, "data": None, "errors": None}
    menu_objs = models.Menu.objects.all().order_by("-id")
    page_objs = page(request, menu_objs)
    if request.method == "GET":
        menu_add_form_obj = forms.MenuForm()
        if request.is_ajax():
            id = request.GET.get("id")
            menu_obj = models.Menu.objects.filter(id=id).values("id", "name", "seq", "comment")
            ret['data'] = list(menu_obj)
            menu_add_form_obj = forms.MenuForm(menu_obj)
            return HttpResponse(json.dumps(ret))
    if request.method == "POST":
        menu_add_form_obj = forms.MenuForm(request.POST)

    return render(request, "juser/menu_list.html",
                  {"page_objs": page_objs,
                   "menu_add_form_obj": menu_add_form_obj,
                   })

@login_required
def menu_add(request):
    """菜单增加"""
    ret = {"status": True, "data": None, "errors": None}
    if request.method == "POST":
        menu_add_form_obj = forms.MenuForm(request.POST)

        if menu_add_form_obj.is_valid():
            models.Menu.objects.create(**menu_add_form_obj.cleaned_data)
        else:
            ret["status"] = False
            ret["errors"] = menu_add_form_obj.errors.as_json()
    return HttpResponse(json.dumps(ret))

@login_required
def menu_edit(request):
    ret = {"status": True, "errors": None}

    if request.method == "POST":
        menu_edit_form_obj = forms.MenuForm(request.POST);
        id=request.POST.get("id");
        if menu_edit_form_obj.is_valid():
            models.Menu.objects.filter(id=id).update(**menu_edit_form_obj.cleaned_data)
        else:
            ret["status"]=False
            ret["errors"]=menu_edit_form_obj.errors.as_json()
    return HttpResponse(json.dumps(ret))

@login_required
def menu_del(request):
    ret = {"status": True, "errors": None}
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            models.Menu.objects.filter(id=id).delete()
        except Exception as e:
            ret["status"] = False
            ret["errors"] = e

    return HttpResponse(json.dumps(ret))

@login_required
def menu2_list(request):
    """二级菜单列表"""

    menu2_objs = models.Menu2.objects.all().order_by("-seq")
    page_objs = page(request, menu2_objs)

    return render(request, "juser/menu2_list.html",
                  {"page_objs": page_objs,})

@login_required
def menu2_add(request):
    """增加二级菜单"""

    if request.method == "GET":
        menu2_form_obj = forms.Menu2Form()

    elif request.method == "POST":
        menu2_form_obj = forms.Menu2Form(request.POST)
        if menu2_form_obj.is_valid():
            models.Menu2.objects.create(**menu2_form_obj.cleaned_data)

            return redirect(reverse("menu2_list"))

    return render(request, "juser/menu2_add.html", {"menu2_form_obj": menu2_form_obj})

@login_required
def menu2_edit(request, id):
    """编辑二级菜单"""

    # 给form初始化值，需要返回的是字典
    menu_obj = models.Menu2.objects.filter(id=id).values()[0]

    if request.method == "GET":
        menu2_form_obj = forms.Menu2Form(initial=menu_obj)

    elif request.method == "POST":

        menu2_form_obj = forms.Menu2Form(request.POST, initial=menu_obj)
        if menu2_form_obj.is_valid():
            models.Menu2.objects.filter(id=id).update(**menu2_form_obj.cleaned_data)

            return redirect(reverse("menu2_list"))

    return render(request, "juser/menu2_edit.html", {"menu2_form_obj": menu2_form_obj})

@login_required
def menu2_del(request):
    """删除二级菜单"""
    ret = {"status": True, "errors": None}
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            models.Menu2.objects.filter(id=id).delete()
        except Exception as e:
            ret["status"] = False
            ret["errors"] = e

    return HttpResponse(json.dumps(ret))

@login_required
def role_list(request):
    """角色列表"""
    if request.method == "GET":
        role_objs = models.Role.objects.all().order_by("-id")
        page_objs = page(request, role_objs)

    return render(request, "juser/role_list.html", {"page_objs": page_objs,})

@login_required
def role_add(request):
    """增加角色"""
    if request.method == "GET":
        role_form_obj = forms.RoleForm()

    elif request.method == "POST":

        role_form_obj = forms.RoleForm(request.POST)
        if role_form_obj.is_valid():
            role_obj = models.Role.objects.create(name=role_form_obj.cleaned_data["name"],
                                                  comment=role_form_obj.cleaned_data["comment"])
            # 多对多关系处理
            role_obj.menu.set(role_form_obj.cleaned_data["menu"])
            role_obj.save()
            return redirect(reverse("role_list"))

    return render(request, "juser/role_add.html", {"role_form_obj": role_form_obj})

@login_required
def role_edit(request, id):
    """编辑角色"""

    role_obj = models.Role.objects.filter(id=id).first()

    # 获取多对多，form验证需要列表
    menu_ids = []
    for menu_id in role_obj.menu.values_list("id"):
        menu_ids.append(menu_id[0])

    # 生成初始化值
    role_dict = {
        "id": role_obj.id,
        "name": role_obj.name,
        "comment": role_obj.comment,
        "menu": menu_ids
    }

    if request.method == "GET":
        role_form_obj = forms.RoleForm(initial=role_dict)

    elif request.method == "POST":
        role_form_obj = forms.RoleForm(request.POST, initial=role_dict)
        if role_form_obj.is_valid():
            role_obj.name = role_form_obj.cleaned_data["name"]
            role_obj.comment = role_form_obj.cleaned_data["comment"]
            # 多对多关系处理
            role_obj.menu.set(role_form_obj.cleaned_data["menu"])
            role_obj.save()
            return redirect(reverse("role_list"))

    return render(request, "juser/role_edit.html", {"role_form_obj": role_form_obj})

@login_required
def role_del(request):
    """删除角色"""
    ret = {"status": True, "errors": None}
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            models.Role.objects.filter(id=id).delete()
        except Exception as e:
            ret["status"] = False
            ret["errors"] = e

    return HttpResponse(json.dumps(ret))
