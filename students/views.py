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
from administrators.decorators import student_only, pin_only
from users.models import *
from administrators.models import Access_Count,E_Pin

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()



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
def pins_settings(request, pk):
    course = Course.objects.get(id=pk)
    cou, created =Settings.objects.get_or_create(id=1)
    if cou.e_pin == False:
        return redirect('exam-details', pk)
    return render(request, 'pins_settings.html',{'course':course})



@login_required(login_url='login_student')
@student_only
def verify_e_pin(request, pk):
    if request.method == 'POST':
        pin_entered = request.POST.get('pin_entered').lower()
        if E_Pin.objects.filter(student=request.user,pin=pin_entered, used=True, expired=False).exists():
            messages.success(request, 'PIN Valid.')
            return redirect('exam-details', pk)
        pins = E_Pin.objects.filter(pin=pin_entered, used=True)
        if pins.exists():
            if pins.filter(student__isnull=False).exclude(student=request.user).exists():
                messages.info(request, 'This PIN has already been used by another student.')
                return redirect('pins_settings', pk)
        expired_pin = E_Pin.objects.filter(student=request.user,pin=pin_entered, used=True, expired=True).first()
        if expired_pin:
            messages.error(request, 'Error: This Pin has expired.')
            return redirect('pins_settings', pk)
        try:
            pin_coun= E_Pin.objects.filter(student=request.user, used=True,expired=False).count()
            if pin_coun > 1:
                messages.info(request, 'You already have an unexpired PIN, Please try the pin that has not be expired')
                return redirect('pins_settings', pk)
            pin = E_Pin.objects.get(pin=pin_entered, used=False, expired=False)
            pin.student = request.user
            pin.used = True
            pin.save()
            messages.success(request, 'PIN successfully validated.')
            return redirect('exam-details', pk)

        except E_Pin.DoesNotExist:
            messages.error(request, 'Error: Invalid PIN.')
            return redirect('pins_settings', pk)
        
        
        

@login_required(login_url='login_student')
@student_only
@pin_only
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
@pin_only
def exam_mode(request, pk):
    user = request.user
    course=Course.objects.get(id=pk)
    if course.exam_control == False:
        messages.error(request, "Exam has error request administrator to turn on 'EXAM SUBMIT'")
        return redirect('exam-details', course.id)
    if course.control == False:
        messages.info(request, 'Exam has not yet be started by the administrator')
        return redirect('exam-details', course.id)
    if user.exam == False:
        messages.info(request, 'Contact the administrator to activate your account')
        return redirect('exam-details', course.id)
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
    cou,created=Settings.objects.get_or_create(id=1)
    if cou.view_result == False:
        messages.info(request, 'This view is disabled by the system administrator')
        return redirect('student_dashboard')
    result = Result.objects.filter(student = request.user).exclude(total_marks = 0)
    return render(request, 'student_course_mark.html', {'result':result})


@login_required(login_url='login_student')
@student_only
def mark(request, pk):
    cou,created=Settings.objects.get_or_create(id=1)
    if cou.view_result == False:
        messages.info(request, 'This view is disabled by the system administrator')
        return redirect('student_dashboard')
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