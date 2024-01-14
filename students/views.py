# builtin import

from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from datetime import timedelta


# app import
from .models import *
from exam.models import *
from administrators.decorators import student_only
from users.models import *
from administrators.models import Access_Count

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()



def login_user(request):
    if request.method == "POST":
        userid = request.POST.get('userid').lower()
        user = authenticate(request, userid=userid, password=request.POST.get('password'))
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


@login_required(login_url='login_student')
@student_only
def pre_video(request):
    return render(request, 'video.html')


@login_required(login_url='login_student')
@student_only
def student_dashboard(request):
    course = Course.objects.filter(department=request.user.department)
    context = {'course':course}
    return render(request, 's_index.html', context)


@login_required(login_url='login_student')
@student_only
def exam_details(request, pk):
    course=Course.objects.get(id=pk)
    total_questions=Question.objects.all().filter(course=course).count()
    questions=Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    hours = course.duration // 60
    minutes = course.duration % 60
    duration = f"{hours:02d} hours : {minutes:02d} minutes"
    context = {'course':course,'total_questions':total_questions,'total_marks':total_marks,'duration':duration}
    return render(request, 'exam_details.html', context)


@login_required(login_url='login_student')
@student_only
def exam_mode(request, pk):
    course=Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course).order_by('?')
    if request.method=='POST':
        pass
    if Result.objects.filter(exam=course,student=request.user, end_time__isnull=False).exists():
        messages.info(request, 'You have already attended this exam')
        return redirect('exam-details', course.id)
    if not questions: 
        messages.error(request, 'Question is not found in this course')
        return redirect('exam-details', course.id)
    if not ExamMode.objects.filter(student=request.user).exists():   
        ExamMode.objects.create(student=request.user)
    if Submitted.objects.filter(student=request.user).exists():
        Submitted.objects.filter(student=request.user).delete()
    if not Result.objects.filter(student=request.user).exists():
        Result.objects.create(
            student = request.user,
            exam = course,
            start_time = timezone.now(),
            marks = 0,
            total_marks = 0,
            missed_marks = 0
        )
    response= render(request,'exam_mode.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response




@login_required(login_url='login_student')
@student_only
def student_course_mark(request):
    result = Result.objects.filter(student = request.user)
    return render(request, 'student_course_mark.html', {'result':result})


@login_required(login_url='login_student')
@student_only
def mark(request, pk):
    result = Result.objects.get(id=pk)
    total_marks = result.marks
    missed_marks = result.missed_marks
    total_mark = total_marks + missed_marks
    num=[total_mark,total_marks,missed_marks]
    if total_mark > 0:
        percent_correct = (total_marks / total_mark) * 100
    else:
        percent_correct = 0
        
    if total_mark > 0:
        percent_missed = (missed_marks / total_mark) * 100
    else:
        percent_missed = 0
        
    num1=[percent_correct,percent_missed]
    context = {'num1':num1,'num':num,'result':result,'percent_correct':percent_correct,'percent_missed':percent_missed}
    return render(request, 'mark.html', context)