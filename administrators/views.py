# builtin import

from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import *
from django.core.exceptions import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash,get_user_model
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
import csv


# app import
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from users.models import *
from exam.models import Course,Result,Question
from students.models import ExamMode,Submitted
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
                next_url =request.GET.get('next')
                return redirect(next_url or 'admin_dashboard')
            elif is_student(user):
                messages.error(request, 'Account with UserID ' + str(request.POST.get('userid')).upper() + ' is not for this view Loggin here')
                return redirect('login_student')
                
        else:
            messages.error(request, 'Account with UserID ' + str(request.POST.get('userid')).upper() + ' not found or Incorrect Password')
    logout(request)
    return render(request, "a_login.html")


def logout_user(request):
    user = request.user
    if user.is_authenticated:
        user.login = False
        user.save()
        if is_student(user):
            logout(request)
            messages.info(request, 'Logout Successful')
            return redirect('login_student')
        logout(request)
        messages.info(request, 'Logout Successful')
        return redirect('login_admin')
    return redirect('login_student')



@login_required(login_url='login_admin')
@admin_only
def count_mode(request):
    mode = ExamMode.objects.all().count()
    submit = Submitted.objects.all().count()
    remain1 = int(mode) - int(submit)
    if remain1 < 0:
        remain = 0
    else:
        remain = int(mode) - int(submit)
    login = User.objects.filter(login=True, groups = Group.objects.get(name='student')).count()
    data = {
        'mode':mode,
        'submit':submit,
        'remain':remain,
        'login':login
    }
    return JsonResponse(data)


@login_required(login_url='login_admin')
@admin_only
def admin_dashboard(request):
    total_student = User.objects.filter(groups = Group.objects.get(name='student')).count()
    total_course = Course.objects.all().count()
    total_department = Department.objects.all().count()
    context = {'total_student':total_student, 'total_course':total_course,'total_department':total_department}
    return render(request, 'a_index.html', context)



# STUDENT VIEW HERE
@login_required(login_url='login_admin')
@admin_only
def all_student(request):
    student = User.objects.filter(groups = Group.objects.get(name='student'))
    department = Department.objects.all()
    myFilter=StudentFilter(request.GET, queryset=student)
    student=myFilter.qs
    context = {'student':student,'department':department}
    return render(request, 'all_student.html', context)

@login_required(login_url='login_admin')
@admin_only
def add_student(request):
    if request.method == 'POST':
        try:
            student = User.objects.create(
                first_name = request.POST.get('first_name').upper(),
                last_name = request.POST.get('last_name').upper(),
                userid = request.POST.get('matric').lower(),               
            )
            student_group = Group.objects.get(name='student')
            student.groups.add(student_group)
            dep = Department.objects.get(name=request.POST.get('department'))
            student.department = dep
            student.save()
            
            messages.success(request, 'Student with Matric NO ' + str(request.POST.get('matric')).upper() + ' successfully Added')
        except:
            messages.error(request, 'Please Make sure that the matric no is not exsiting ')

        next_url =request.GET.get('next')
        return redirect(next_url or 'all-student')
    pass



@login_required(login_url='login_admin')
@admin_only
def del_student(request):
    if request.method == 'POST':
        matric = request.POST.get('matric').lower()
        try:
            stu=User.objects.get(userid=matric)
            stu.delete()
            messages.success(request, 'Student has been deleted successfully')
        except:
            messages.error(request, 'Student with Matric NO ' + str(request.POST.get('matric')).upper() + ' not found')
        next_url =request.GET.get('next')
        return redirect(next_url or 'all-student')
    pass

@login_required(login_url='login_admin')
@admin_only
def del_student1(request, pk):
    stu=User.objects.get(id=pk)
    stu.delete()
    messages.success(request, 'Student has been deleted successfully')
    next_url =request.GET.get('next')
    return redirect(next_url or 'all-student')

@login_required(login_url='login_admin')
@admin_only
def del_all_student(request):
    stu=User.objects.filter(groups=Group.objects.get(name='student'))
    stu.delete()
    messages.success(request, 'All Students has been deleted successfully')
    next_url =request.GET.get('next')
    return redirect(next_url or 'all-student')



@login_required(login_url='login_admin')
@admin_only
def import_students(request):
    department = Department.objects.all()
    context = {'department':department}
    return render(request, 'import_students.html', context)


@login_required(login_url='login_admin')
@admin_only
def department(request):
    department = Department.objects.all()
    context = {'department':department}
    return render(request, 'department.html', context)


@login_required(login_url='login_admin')
@admin_only
def add_department(request):
    if request.method == 'POST':
        try:
            Department.objects.create(
                name = request.POST.get('department').upper()
            )
            
            messages.success(request, request.POST.get('department').upper() + ' Added successfully')
        except:
            messages.error(request, 'Department all ready exist')
            
        next_url =request.GET.get('next')
        return redirect(next_url or 'department')

@login_required(login_url='login_admin')
@admin_only
def del_department(request, pk):
    dep=Department.objects.get(id=pk)
    dep.delete()
    messages.success(request, dep.name +' successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'department')


@login_required(login_url='login_admin')
@admin_only
def import_courses(request):
    department = Department.objects.all()
    context = {'department':department}
    return render(request, 'import_courses.html', context)



@login_required(login_url='login_admin')
@admin_only
def add_course(request):
    if request.method == 'POST':
        try:
            cou = Course.objects.create(
                name = request.POST.get('name'),
                total_marks = request.POST.get('mark'),
                duration = request.POST.get('duration')
            )
            dep = Department.objects.get(name=request.POST.get('department'))
            cou.department = dep
            cou.save()
            messages.success(request, request.POST.get('name').upper() + ' Added successfully')
        except:
            messages.error(request, 'Course already exist or duration error or invalid department')
            
        next_url =request.GET.get('next')
        return redirect(next_url or 'course')

@login_required(login_url='login_admin')
@admin_only
def del_course(request, pk):
    cou=Course.objects.get(id=pk)
    cou.delete()
    messages.success(request, cou.name +' successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'course')

@login_required(login_url='login_admin')
@admin_only
def course(request):
    course=Course.objects.all()
    department = Department.objects.all()
    context = {'course':course,'department':department}
    return render(request, 'course.html', context)

@login_required(login_url='login_admin')
@admin_only
def del_all_courses(request):
    cou=Course.objects.all()
    cou.delete()
    messages.success(request,'All courses successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'course')



@login_required(login_url='login_admin')
@admin_only
def add_question(request):
    if request.method == 'POST':
        try:
            question = Question.objects.create(
                marks = request.POST.get('mark'),
                question = request.POST.get('question'),
                option1 = request.POST.get('option1'),
                option2 = request.POST.get('option2'),
                option3 = request.POST.get('option3'),
                option4 = request.POST.get('option4'),
                answer = request.POST.get('answer')
            )
            cou = Course.objects.get(name=request.POST.get('course'))
            question.course = cou
            question.save()
            messages.success(request, request.POST.get('question').upper() + ' Added successfully')
        except:
            messages.error(request, 'Question already exist or options error or invalid course')
            
        next_url =request.GET.get('next')
        return redirect(next_url or 'question')


@login_required(login_url='login_admin')
@admin_only
def question(request):
    course=Course.objects.all()
    context = {'course':course}
    return render(request, 'question.html', context)


@login_required(login_url='login_admin')
@admin_only
def question_details(request, pk):
    course=Course.objects.get(id=pk)
    hours = course.duration // 60
    minutes = course.duration % 60
    duration = f"{hours:02d} hours : {minutes:02d} minutes"
    question = Question.objects.filter(course=course)
    if not question:
        messages.info(request, 'Question can not be found for ' + course.name)
        return redirect('question')
    total_questions=Question.objects.all().filter(course=course).count()
    total_marks=0
    for q in question:
        total_marks=total_marks + q.marks
    context = {'course':course,'total_questions':total_questions,'total_marks':total_marks,'question':question,'duration':duration}
    return render(request, 'question_details.html', context)


@login_required(login_url='login_admin')
@admin_only
def import_question(request):
    course=Course.objects.all()
    context = {'course':course}
    return render(request, 'import_question.html', context)


@login_required(login_url='login_admin')
@admin_only
def del_all_question(request):
    que=Question.objects.all()
    que.delete()
    messages.success(request,'All Question successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'question')

@login_required(login_url='login_admin')
@admin_only
def del_course_question(request, name):
    course=Course.objects.get(name=name)
    question = Question.objects.filter(course=course)
    question.delete()
    messages.success(request,'All Questions for ' + str(course.name) + ' successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'question')

@login_required(login_url='login_admin')
@admin_only
def all_results(request):
    result = Result.objects.all()
    department = Department.objects.all()
    course = Course.objects.all()
    myFilter=ResultFilter(request.GET, queryset=result)
    result=myFilter.qs
    return render(request, 'all_results.html', {'result':result,'course':course,'department':department})

@login_required(login_url='login_admin')
@admin_only
def filter_results_download(request):
    result = Result.objects.all()
    myFilter=ResultFilter(request.GET, queryset=result)
    result=myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="imported_results.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Result._meta.fields]
    csv_writer.writerow(header_row)
    
    for result in result:
        data_row = [str(getattr(result, field_name.name)) for field_name in Result._meta.fields]
        csv_writer.writerow(data_row)
    return response
        


@login_required(login_url='login_admin')
@admin_only
def admin_view_mark(request, pk):
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
    return render(request, 'admin_view_mark.html', context)

@login_required(login_url='login_admin')
@admin_only
def del_all_results(request):
    result=Result.objects.all()
    result.delete()
    messages.success(request,'All Results successfully Reset')
    next_url =request.GET.get('next')
    return redirect(next_url or 'all_results')


@login_required(login_url='login_admin')
@admin_only
def del_result(request, pk):
    result=Result.objects.get(id=pk)
    result.delete()
    messages.success(request, str(result.student) +' successfully Reset')
    next_url =request.GET.get('next')
    return redirect(next_url or 'all_results')



def decline(request):
    return render(request, 'decline.html')



def changepassword(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password has been changed successfully')
                return redirect('changepassword')
            else:
                messages.error(request, 'Incorrect old password or password mismatch' )
        
        return render(request, 'changepassword.html')
    return redirect('login_student')