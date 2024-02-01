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
from administrators.decorators import admin_only,student_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

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
        response['Content-Disposition'] = 'attachment; filename=Student Template.xlsx'
    
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
        response['Content-Disposition'] = 'attachment; filename=Course Template.xlsx'
    
    return response

@login_required(login_url='login_admin')
@admin_only
def excel_download2(request):
    excel_file_path = finders.find('template_sample2.xlsx')

    # Check if the file exists
    if not excel_file_path:
        raise FileNotFoundError(f"The file 'Objective Question Template.xlsx.xlsx' was not found in the static files.")

    # Open the Excel file in binary mode
    with open(excel_file_path, 'rb') as file:
        # Create an HTTP response with the Excel content
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Objective Question Template.xlsx'
    
    return response


@admin_only
def excel_download3(request):
    excel_file_path = finders.find('template_sample3.xlsx')

    # Check if the file exists
    if not excel_file_path:
        raise FileNotFoundError(f"The file 'Theory Question Template.xlsx.xlsx' was not found in the static files.")

    # Open the Excel file in binary mode
    with open(excel_file_path, 'rb') as file:
        # Create an HTTP response with the Excel content
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Theory Question Template.xlsx'
    
    return response






@login_required(login_url='login_admin')
@admin_only
def verify_student_student(request):
    return render(request, 'verify_student_info.html')
 
@login_required(login_url='login_admin')
@admin_only
def verify_course_info(request):
    return render(request, 'verify_course_info.html')


@login_required(login_url='login_student')
@student_only
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
        hours = course.duration // 60
        minutes = course.duration % 60
        duration = f"{hours:02d} hours : {minutes:02d} minutes"
        view_result,created=Settings.objects.get_or_create(id=1)
        cou = view_result.view_result
        context = {'num1':num1,'num':num,'course':course,'percent_correct':percent_correct,
                   'percent_missed':percent_missed,'total_marks':total_marks,'duration':duration,'questions':questions,
                   'total_mark':total_mark,'missed_marks':missed_marks,'total_marks':total_marks,'cou':cou}
        return render(request, 'view_mark.html', context)
    else:
        messages.info(request,'you can now view your mark in the view mark button at the navbar')
        return redirect('student_dashboard')
    
    

@login_required(login_url='login_student')
@student_only
def access_mode(request,pk):
    stu=request.user.exam
    course = Course.objects.get(id = pk)
    control = course.control
    end_exam = course.exam_control
    setting = Settings.objects.get(id=1)
    stop_time = setting.stop_time
    print(stop_time)
    
    data = {
        'stu':stu,
        'end_exam':end_exam,
        'control':control,
        'stop_time':stop_time
    }
    return JsonResponse(data)



def generate_pdf(request):
    #if request.COOKIES.get('course_ID') is not None:
    #course_id = request.COOKIES.get('course_ID')
    course=Course.objects.get(id=1)
    questions_pdfs = Theory_Question.objects.filter(course=course, student=request.user)
    
    school_info = School_Info.objects.first()

    # Create a BytesIO buffer to store the PDF content
    buffer = BytesIO()

    # Create the PDF object using ReportLab
    p = canvas.Canvas(buffer, pagesize=A4)

    # Set font style to bold
    p.setFont("Helvetica-Bold", 12)

    # Center the school information
    school_info_text = school_info.name.upper() + school_info.address.upper() + school_info.semester.upper()
    school_info_width = p.stringWidth(school_info_text, "Helvetica-Bold", 12)
    x_position = (A4[0] - school_info_width) / 2
    p.drawString(x_position, 800, school_info_text)

    # Reset font style
    p.setFont("Helvetica", 12)
    # Iterate over questions_pdfs and add content to the PDF
    y_position = 660
    for question_pdf in questions_pdfs:
        question_text = question_pdf.question
        student_answer = question_pdf.student_answer

        p.drawString(100, y_position, f"Question: {question_text}")
        p.drawString(100, y_position - 20, f"Student Answer: {student_answer}")
        y_position -= 40

    # Save the PDF to the buffer
    p.showPage()
    p.save()

    # Rewind the buffer to the beginning
    buffer.seek(0)

    # Create a Django response and return the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="exam_result.pdf"'
    response.write(buffer.read())

    return response


@login_required(login_url='login_student')
def soon(request):
    
    return render(request,'coming_soon.html')