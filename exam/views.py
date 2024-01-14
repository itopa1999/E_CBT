from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.templatetags.static import static
import os
from django.contrib.staticfiles import finders
from .models import *
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from students.models import ExamMode, Submitted
from administrators.decorators import admin_only
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login_admin')
@admin_only
def excel_download(request):
    excel_file_path = finders.find('template_sample.xlsx')

    # Check if the file exists
    if not excel_file_path:
        raise FileNotFoundError(f"The file 'template_sample.xlsx' was not found in the static files.")

    # Open the Excel file in binary mode
    with open(excel_file_path, 'rb') as file:
        # Create an HTTP response with the Excel content
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=template_sample.xlsx'
    
    return response


@login_required(login_url='login_admin')
@admin_only
def excel_download1(request):
    excel_file_path = finders.find('templete_sample1.xlsx')

    # Check if the file exists
    if not excel_file_path:
        raise FileNotFoundError(f"The file 'template_sample.xlsx' was not found in the static files.")

    # Open the Excel file in binary mode
    with open(excel_file_path, 'rb') as file:
        # Create an HTTP response with the Excel content
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=template_sample.xlsx'
    
    return response

@login_required(login_url='login_admin')
@admin_only
def excel_download2(request):
    excel_file_path = finders.find('template_sample2.xlsx')

    # Check if the file exists
    if not excel_file_path:
        raise FileNotFoundError(f"The file 'template_sample.xlsx' was not found in the static files.")

    # Open the Excel file in binary mode
    with open(excel_file_path, 'rb') as file:
        # Create an HTTP response with the Excel content
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=template_sample.xlsx'
    
    return response



@login_required(login_url='login_admin')
@admin_only
def verify_student_student(request):
    return render(request, 'verify_student_info.html')
 
@login_required(login_url='login_admin')
@admin_only
def verify_course_info(request):
    return render(request, 'verify_course_info.html')

@login_required(login_url='login_admin')
@admin_only
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=Course.objects.get(id=course_id)
        if Result.objects.filter(exam=course,student=request.user, end_time__isnull=False).exists():
            messages.info(request, 'You have already attended this exam')
            return redirect('exam-details', course.id)
        total_marks=0
        total_mark = 0 
        questions=Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            total_mark += questions[i].marks
        for i in range(len(questions)):
            selected_ans_key = str(questions[i].id)
            selected_ans = request.COOKIES.get(selected_ans_key)
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks += questions[i].marks
            missed_marks = total_mark - total_marks
        result = Result.objects.filter(exam=course, student=request.user).first()
        if result is not None:
            result.marks=total_marks
            result.missed_marks = missed_marks
            result.end_time = timezone.now()
            result.total_marks = int(result.missed_marks) + (result.marks)
            time_used_seconds = (result.end_time - result.start_time).total_seconds()
            result.time_used = timedelta(seconds=int(time_used_seconds))
            total_exam_duration_minutes = course.duration
            time_remaining_minutes = max(total_exam_duration_minutes - time_used_seconds // 60, 0)
            result.time_remaining = timedelta(minutes=int(time_remaining_minutes))
            result.save()
        else:
            messages.error(request, 'sorry we can get your record from the database, please contact your administrator')
            return redirect('exam-details', course.id)
        ExamMode.objects.filter(student=request.user).delete()
        Submitted.objects.create(student=request.user)
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
        context = {'num1':num1,'num':num,'course':course,'percent_correct':percent_correct,'percent_missed':percent_missed}
        return render(request, 'view_mark.html', context)
    else:
        messages.info(request,'you can now view your mark in the view mark button at the navbar')
        return redirect('student_dashboard')
    