from django.shortcuts import redirect
from .models import E_Pin
from exam.models import Settings
from django.contrib import messages


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            return redirect('decline')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function


def student_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('decline')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function


def pin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        cou, created =Settings.objects.get_or_create(id=1)
        if E_Pin.objects.filter(student=request.user, used=True, expired=False).exists() and cou.e_pin == True:
            return view_func(request, *args,**kwargs)
        elif cou.e_pin == False:
            return view_func(request, *args,**kwargs)
        else:
            messages.info(request, 'Please verify your pin again.')
            return redirect('student_dashboard')
    return wrapper_function