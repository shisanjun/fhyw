from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, authenticate
from django.urls import reverse
from juser import models
from utils.pages import page
from juser import forms
import json


# Create your views here.

def index(request):
    print("xxx")
    return render(request, "muban.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return redirect(reverse("index"))

    return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect(reverse("login"))


def user_list(request):
    user_objs = models.UserProfile.objects.all()
    page_objs = page(request, user_objs, 1)
    return render(request, "juser/user_list.html", {"page_objs": page_objs})


def user_add(request):
    if request.method == "GET":
        user_form_obj = forms.UserProfileForm()

    elif request.method == "POST":
        user_form_obj = forms.UserProfileForm(request.POST)

    return render(request, "juser/user_add.html", {"user_form_obj": user_form_obj})


def menu_list(request):
    """菜单列表"""
    menu_objs = models.Menu.objects.all().order_by("-id")
    page_objs = page(request, menu_objs, 2)

    menu_add_form_obj = forms.MenuForm()

    return render(request, "juser/menu_list.html",
                  {"page_objs": page_objs,
                   "menu_add_form_obj": menu_add_form_obj,
                   })


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


def menu_edit(request):
    pass


def menu_del(request):
    ret = {"status": True, "errors": None}
    if request.method=="GET":
        id=request.GET.get("id")
        try:
            models.Menu.objects.filter(id=id).delete()
        except Exception as e:
            ret["status"]=False
            ret["errors"]=e

    return HttpResponse(json.dumps(ret))


