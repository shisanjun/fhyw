from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.urls import reverse
from juser import models
from utils.pages import page
from juser.forms import UserProfileForm


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
    if request.method=="GET":
        user_form_obj = UserProfileForm()

    elif request.method == "POST":
        user_form_obj = UserProfileForm(request.POST)

    return render(request, "juser/user_add.html", {"user_form_obj": user_form_obj})


def menu_list(request):
    menu_objs = models.Menu.objects.all()
    page_objs = page(request, menu_objs, 2)
    return render(request, "juser/menu_list.html", {"page_objs": page_objs})
