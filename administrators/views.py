# builtin import

from django.shortcuts import render, redirect
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
from reportlab.pdfgen import canvas
from io import BytesIO

# app import
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from users.models import *
from exam.models import Course,Result,Question, Settings
from students.models import ExamMode,Submitted
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()



def login_user(request):
    if request.method == "POST":
        userid = request.POST.get('userid').upper()
        user = authenticate(request, userid=userid, password=request.POST.get('password').lower())
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
    cou, created =Settings.objects.get_or_create(id=1)
    exam = Course.objects.filter(control=True).count() == Course.objects.all().count()
    exam_submit = Course.objects.filter(exam_control=True).count() == Course.objects.all().count()
    student_permission = User.objects.filter(exam=True, groups = Group.objects.get(name='student')).count() == User.objects.filter(groups = Group.objects.get(name='student')).count()
    context = {'total_student':total_student, 'total_course':total_course,'exam_submit':exam_submit,'student_permission':student_permission,
               'total_department':total_department,'exam':exam,'cou':cou}
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
def edit_student(request, pk):
    stu=User.objects.get(id=pk)
    form = UserChangeForm(instance = stu)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=stu)
        if form.is_valid():
            form.save()
            messages.success(request, str(stu.first_name) +' successfully update')
        messages.error(request, form.errors)
    context = {'stu':stu,'form':form}
    return render(request, 'edit_student.html', context)



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
    level = Level.objects.all()
    context = {'department':department,'level':level}
    return render(request, 'department.html', context)


@login_required(login_url='login_admin')
@admin_only
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('department').upper()
        levels = Level.objects.all()
        for index, level in enumerate(levels):
            try:
                department_name = f"{name} - Department {level.name}"
                Department.objects.create(
                    name = department_name,
                    level = level
                )
            except:
                messages.error(request, 'Department all ready exist')
        messages.success(request, request.POST.get('department').upper() + ' Added successfully')
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
            dep = Department.objects.filter(name__in=request.POST.getlist('department'))
            for dep in dep:
                cou.department.add(dep)
                cou.save()
            messages.success(request, request.POST.get('name').upper() + ' Added successfully')
        except:
            messages.error(request, 'Course already exist or duration error or invalid department')
            
        next_url =request.GET.get('next')
        return redirect(next_url or 'course')


@login_required(login_url='login_admin')
@admin_only
def edit_course(request, pk):
    cou=Course.objects.get(id=pk)
    form = CourseForm(instance=cou)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=cou)
        if form.is_valid():
            form.save()
            messages.success(request, str(cou.name) +' successfully update')
        messages.error(request, form.errors)
    context = {'form':form,'cou':cou}
    return render(request, 'edit_course.html', context)



@login_required(login_url='login_admin')
@admin_only
def course(request):
    course=Course.objects.all()
    department = Department.objects.all()
    level = Level.objects.all()
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    context = {'course':course,'department':department,'level':level}
    return render(request, 'course.html', context)







@login_required(login_url='login_admin')
@admin_only
def add_question(request):
    if request.method == 'POST':
        try:
            question = Question.objects.create(
                marks = request.POST.get('mark'),
                question = request.POST.get('question'),
                A = request.POST.get('A'),
                B = request.POST.get('B'),
                C = request.POST.get('C'),
                D = request.POST.get('D'),
                answer = request.POST.get('answer')
            )
            cou = Course.objects.filter(name__in=request.POST.getlist('course'))
            for cou in cou:
                cou.exam_control = True
                cou.control = False
                cou.save()
                question.course.add(cou)
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
    department = Department.objects.all()
    level = Level.objects.all()
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    context = {'course':course,'department':department,'level':level}
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
    cou = Course.objects.all()
    for cou in cou:
        cou.exam_control = True
        cou.control = False
        cou.save()
    messages.success(request,'All Question successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'question')

@login_required(login_url='login_admin')
@admin_only
def del_course_question(request, name):
    course=Course.objects.get(name=name)
    course.exam_control = True
    course.control = False
    course.save()
    question = Question.objects.filter(course=course)
    question.delete()
    messages.success(request,'All Questions for ' + str(course.name) + ' successfully deleted')
    next_url =request.GET.get('next')
    return redirect(next_url or 'question')

@login_required(login_url='login_admin')
@admin_only
def all_results(request):
    result = Result.objects.exclude(total_marks = 0)
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
    response['Content-Disposition'] = 'attachment; filename ="Reult.csv"'
    
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
    questions = Question.objects.filter(course=result.exam)
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
    context = {'num1':num1,'num':num,'result':result,'percent_correct':percent_correct,'percent_missed':percent_missed,
               'questions':questions}
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



@login_required(login_url='login_admin')
@admin_only
def submitmode(request):
    mode = Submitted.objects.all()
    department = Department.objects.all()
    myFilter=SubmittedFilter(request.GET, queryset=mode)
    mode=myFilter.qs
    return render(request, 'submitmode.html', {'mode':mode,'department':department})


@login_required(login_url='login_admin')
@admin_only
def exammode(request):
    mode = ExamMode.objects.all()
    department = Department.objects.all()
    myFilter=ExamModeFilter(request.GET, queryset=mode)
    mode=myFilter.qs
    return render(request, 'exammode.html', {'mode':mode,'department':department})

@login_required(login_url='login_admin')
@admin_only
def studentaccess(request):
    student = User.objects.filter(groups = Group.objects.get(name='student'))
    department = Department.objects.all()
    myFilter=StudentFilter(request.GET, queryset=student)
    student=myFilter.qs
    return render(request, 'studentaccess.html', {'student':student,'department':department})

@login_required(login_url='login_admin')
@admin_only
def activate_student(request, pk):
    user = User.objects.get(id = pk)
    user.exam = True
    user.save()
    messages.success(request, 'Students has been successfully Activated to writing the exam')
    return redirect('studentaccess')

@login_required(login_url='login_admin')
@admin_only
def deactivate_student(request, pk):
    user = User.objects.get(id = pk)
    user.exam = False
    user.save()
    messages.success(request, 'Students has been successfully Deactivated from writing the exam')
    return redirect('studentaccess')




@login_required(login_url='login_admin')
@admin_only
def examaccess(request):
    course=Course.objects.all().order_by('control')
    department = Department.objects.all()
    level = Level.objects.all()
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    context = {'course':course,'department':department,'level':level}
    return render(request, 'examaccess.html',context)

@login_required(login_url='login_admin')
@admin_only
def startexam(request, pk):
    course = Course.objects.get(id = pk)
    course.control = True
    course.save()
    messages.success(request, 'Students can now start ' + str(course.name) + ' Exam now')
    return redirect('examaccess')

@login_required(login_url='login_admin')
@admin_only
def unstartexam(request, pk):
    course = Course.objects.get(id = pk)
    course.control = False
    course.save()
    messages.success(request, 'All Students Writing ' + str(course.name) + ' exam will be kicked out of the exam')
    return redirect('examaccess')

@login_required(login_url='login_admin')
@admin_only
def endexam(request, pk):
    course = Course.objects.get(id = pk)
    course.exam_control = False
    course.save()
    messages.success(request, 'All Students Writing ' + str(course.name) + 'exam will be auto submitted')
    return redirect('examaccess')


@login_required(login_url='login_admin')
@admin_only
def unendexam(request, pk):
    course = Course.objects.get(id = pk)
    course.exam_control = True
    course.save()
    messages.success(request, 'Successfully Un-end exam, students can now write exams')
    return redirect('examaccess')

@login_required(login_url='login_admin')
@admin_only
def levels(request):
    level = Level.objects.all()
    return render(request, 'levels.html', {'level':level})

@login_required(login_url='login_admin')
@admin_only
def add_level(request):
    if request.method == 'POST':
        try:
            Level.objects.create(
                name = request.POST.get('name').upper()
            )
            messages.success(request, 'Level ' + str(request.POST.get('name').upper()) + ' successfully added')
        except:
            messages.error(request, 'Level ' + str(request.POST.get('name').upper()) + ' may already exist')
        next_url =request.GET.get('next')
        return redirect(next_url or 'levels')
    pass



def decline(request):
    return render(request, 'decline.html')


@login_required(login_url='student_admin')
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


#...........................................................................


@login_required(login_url='login_admin')
@admin_only
def exam_per_on(request):
    cou = Course.objects.all()
    cou.update(control = True)
    messages.success(request,'All Course has been set to start exam')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')


@login_required(login_url='login_admin')
@admin_only
def exam_per_off(request):
    cou = Course.objects.all()
    cou.update(control = False)
    messages.success(request,'All Course has been set to not start exam')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def exam_submit_on(request):
    cou = Course.objects.all()
    cou.update(exam_control = True)
    messages.success(request,'All Exams set to normal')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')


@login_required(login_url='login_admin')
@admin_only
def exam_submit_off(request):
    cou = Course.objects.all()
    cou.update(exam_control = False)
    messages.success(request,'All Exams will be submitted Automatically')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')


@login_required(login_url='login_admin')
@admin_only
def student_permission_on(request):
    cou = User.objects.filter(groups = Group.objects.get(name='student'))
    cou.update(exam = True)
    messages.success(request,'All Student can start exam')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def student_permission_off(request):
    cou = User.objects.filter(groups = Group.objects.get(name='student'))
    cou.update(exam = False)
    messages.success(request,'All Student cannot start exam')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def view_result_on(request):
    cou,created=Settings.objects.get_or_create(id=1)
    cou.view_result = True
    cou.save()
    messages.success(request,'All Students can view Result')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def view_result_off(request):
    cou,created=Settings.objects.get_or_create(id=1)
    cou.view_result = False
    cou.save()
    messages.success(request,'All Students cannot view Result.')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def stop_time_on(request):
    cou,created=Settings.objects.get_or_create(id=1)
    cou.stop_time = True
    cou.save()
    messages.success(request,'All Exam time has been paused.')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')


@login_required(login_url='login_admin')
@admin_only
def stop_time_off(request):
    cou,created=Settings.objects.get_or_create(id=1)
    cou.stop_time = False
    cou.save()
    messages.success(request,'All Exam time will start or continue.')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def filter_start_exam_on(request):
    course=Course.objects.all().order_by('control')
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    course.update(control = True)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('examaccess')


@login_required(login_url='login_admin')
@admin_only
def filter_start_exam_off(request):
    course=Course.objects.all().order_by('control')
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    course.update(control = False)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('examaccess')



@login_required(login_url='login_admin')
@admin_only
def filter_exam_submit_on(request):
    course=Course.objects.all().order_by('control')
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    course.update(exam_control = True)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('examaccess')



@login_required(login_url='login_admin')
@admin_only
def filter_exam_submit_off(request):
    course=Course.objects.all().order_by('control')
    myFilter=CourseFilter(request.GET, queryset=course)
    course=myFilter.qs
    course.update(exam_control = False)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('examaccess')



@login_required(login_url='login_admin')
@admin_only
def filter_student_permission_on(request):
    student = User.objects.filter(groups = Group.objects.get(name='student'))
    myFilter=StudentFilter(request.GET, queryset=student)
    student=myFilter.qs
    student.update(exam = True)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('studentaccess')



@login_required(login_url='login_admin')
@admin_only
def filter_student_permission_off(request):
    student = User.objects.filter(groups = Group.objects.get(name='student'))
    myFilter=StudentFilter(request.GET, queryset=student)
    student=myFilter.qs
    student.update(exam = False)
    messages.success(request, 'filtered Value has been updated accordindly')
    return redirect('studentaccess')



def tc(request):
    return render(request, 'tc.html')



@login_required(login_url='login_admin')
@admin_only
def e_pin_off(request):
    cou, created =Settings.objects.get_or_create(id=1)
    cou.e_pin = False
    cou.save()
    messages.success(request, 'E-Pin Feature turn off')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')



@login_required(login_url='login_admin')
@admin_only
def e_pin_on(request):
    cou, created =Settings.objects.get_or_create(id=1)
    cou.e_pin = True
    cou.save()
    messages.success(request, 'E-Pin Feature turn on')
    next_url =request.GET.get('next')
    return redirect(next_url or 'admin_dashboard')


@login_required(login_url='login_admin')
@admin_only
def expire_pins(request):
    pin = E_Pin.objects.filter(used = True)
    pin.update(expired=True)
    messages.success(request, 'All used pins has been set to expired')
    next_url =request.GET.get('next')
    return redirect(next_url or 'e-pin')



@login_required(login_url='login_admin')
@admin_only
def e_pin(request):
    pin = E_Pin.objects.all()
    myFilter=PinFilter(request.GET, queryset=pin)
    pin=myFilter.qs
    context = {'pin':pin}
    return render(request, 'e_pin.html', context)

@login_required(login_url='login_admin')
@admin_only
def generate_pins(request):
    cou, created =Settings.objects.get_or_create(id=1)
    if cou.e_pin == True:
        unassigned_unused_pins = E_Pin.objects.unassigned_and_unused_pins()
        if unassigned_unused_pins.exists():
            messages.info(request, "There's still "+ str(unassigned_unused_pins.count()) + " Unused Pins")
            return redirect('e-pin')
        for _ in range(50):
            random_number = random.randint(1000000000, 9999999999)
            instance = E_Pin(pin=f'ajp{random_number}')
            instance.save()
        messages.success(request, 'Pins Generated')
    messages.error(request, 'You must have to turn this feature on in the setting')
    return redirect('e-pin')
        

def generate_unused_pin_pdf(request):
    # Get unassigned and unused pins using the custom manager
    unassigned_unused_pins = E_Pin.objects.unassigned_and_unused_pins()

    # Create a BytesIO buffer to write the PDF
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    pdf = canvas.Canvas(buffer)

    # Set the page size
    page_width, page_height = 612, 792  # Standard letter size (8.5 x 11 inches)
    pdf.setPageSize((page_width, page_height))

    # Set initial y_position
    y_position = page_height - 50

    # Add a title to the first page
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, y_position, "UNUSED PIN")

    # Add a counter for each pin on multiple pages
    pdf.setFont("Helvetica", 12)
    counter = 1

    for pin in unassigned_unused_pins:
        if y_position <= 50:
            # Start a new page
            pdf.showPage()
            y_position = page_height - 50
        pdf.drawString(100, y_position - 20, f"{counter}. {pin.pin}")
        y_position -= 20
        counter += 1

    # Save the PDF content
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="unused_pins.pdf"'
    return response


@login_required(login_url='login_admin')
@admin_only
def edit_level(request,pk):
    pass


@login_required(login_url='login_admin')
@admin_only
def edit_department(request,pk):
    pass


@login_required(login_url='login_admin')
@admin_only
def actions(request):
    return render(request, 'actions.html')



