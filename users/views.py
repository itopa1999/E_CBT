# builtin import

from django.shortcuts import render, redirect
from django.core.paginator import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.core.exceptions import *


# app import

from .models import *


# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()



def login_user(request):
    if request.method == "POST":
        userid = request.POST.get('userid').lower()
        user = authenticate(request, userid=userid, password=request.POST.get('password').lower())
        if user is not None:
            login(request, user)
            user.login = True
            user.save()
            if is_admin(user):
                messages.error(request, 'Account with UserID ' + str(request.POST.get('userid')).upper() + ' is not for this view Loggin here')
                return redirect('login_admin')
            elif is_student(user):
                next_url =request.GET.get('next')
                return redirect(next_url or 'student_dashboard')
        else:
            messages.error(request, 'Account with UserID ' + str(request.POST.get('userid')).upper() + ' not found or Incorrect Password')
    try:
        if request.user.is_authenticated:
            user = request.user
            user.login = False
            user.save()
    except Exception as e:
        print("Error:", e)
    logout(request)
    return render(request, "s_login.html")