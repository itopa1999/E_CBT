from .resources import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from .resources import *
from tablib import Dataset
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from users.models import User, Department
from .models import Course, Theory_Question, Question

def import_student_data(request):
    if request.method == 'POST':
        dep = Department.objects.get(name=request.POST.get('department'))
        resource = UserFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return redirect('import-students')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
            
        department_data = []
        headers = imported_data.headers

        for row in imported_data:
            row_dict = dict(zip(headers, row))
            row_dict['department'] = request.POST.get('department')
            department_data.append(row_dict)
            

        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json
            request.session['imported_department'] = dep.name
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'verify_student_info.html', {'data': department_data, 'count': count, 'new_data': new_data})
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-students')


def verify_data(request):
    imported_data_json = request.session.get('imported_data', None)
    imported_dapartment = request.session.get('imported_department', None)
    
    if not imported_data_json:
        return redirect('import-students')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = UserFile()
        result = resource.import_data(dataset, dry_run=False)
        if not result.has_errors():
            userid_values = [row[2] for row in dataset]
            for user in userid_values:
                user = User.objects.get(userid=user)
                group= Group.objects.get(name='student')
                user.groups.add(group)
                dep = Department.objects.get(name=imported_dapartment)
                user.department = dep
                user.save()
            messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-students')





def import_courses_data(request):
    if request.method == 'POST':
        dep = request.POST.getlist('department')
        resource = CourseFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return redirect('import-courses')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
            
        department_data = []
        headers = imported_data.headers

        for row in imported_data:
            row_dict = dict(zip(headers, row))
            row_dict['department'] = request.POST.getlist('department')
            department_data.append(row_dict)
            

        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json
            request.session['imported_department'] = dep
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'verify_course_info.html', {'data': department_data, 'count': count, 'new_data': new_data})
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-courses')


def verify_data1(request):
    imported_data_json = request.session.get('imported_data', None)
    imported_dapartment = request.session.get('imported_department', None)
    if not imported_data_json:
        return redirect('import-courses')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = CourseFile()
        result = resource.import_data(dataset, dry_run=False)
        if not result.has_errors():
            dep = Department.objects.filter(name__in=imported_dapartment)
            for dep in dep:
                course_values = [row[0] for row in dataset]
                for course in course_values:
                    cou = Course.objects.get(name=course)
                    cou.department.add(dep)
                    cou.save()
                messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-courses')




def import_question_data(request):
    if request.method == 'POST':
        cou = request.POST.getlist('course')
        resource = QuestionFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return redirect('import-question')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
            
        course_data = []
        headers = imported_data.headers

        for row in imported_data:
            row_dict = dict(zip(headers, row))
            row_dict['course'] = cou
            course_data.append(row_dict)
            

        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            request.session['imported_data'] = dataset.json
            request.session['imported_course'] = cou
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'verify_question_info.html', {'data': course_data, 'count': count, 'new_data': new_data})
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-question')



def verify_data2(request):
    imported_data_json = request.session.get('imported_data', None)
    imported_course = request.session.get('imported_course', None)
    if not imported_data_json:
        return redirect('import-question')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = QuestionFile()
        result = resource.import_data(dataset, dry_run=False)
        if not result.has_errors():
            cou = Course.objects.filter(name__in=imported_course)
            for cou in cou:
                cou.exam_control = False
                cou.control = False
                cou.save()
                question_values = [row[0] for row in dataset]
                for question in question_values:
                    que = Question.objects.get(question=question)
                    que.course.add(cou)
                    que.save()
            messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-question')





def import_theory_question_data(request):
    if request.method == 'POST':
        cou = request.POST.getlist('course')
        resource = TheoryQuestionFile()
        dataset = Dataset()
        new_data = request.FILES['import_file']
        file_extension = new_data.name.split('.')[-1].lower()
        if  new_data.name.endswith('csv')  or  new_data.name.endswith('xlsx'):
            pass
        else:
            messages.error(request, 'File must be in csv or xlsx format')
            return redirect('import-question')
        formats_mapping = {
            'csv': 'csv',
            'xlsx': 'xlsx',
        }

        selected_format = formats_mapping[file_extension]

        if file_extension == 'xlsx':
            imported_data = dataset.load(new_data.read(), format=selected_format)
        else:
            imported_data = dataset.load(new_data.read().decode('utf-8'), format=selected_format)
        course_data = []
        headers = imported_data.headers
        for row in imported_data:
            row_dict = dict(zip(headers, row))
            row_dict['course'] = cou
            course_data.append(row_dict)
        result = resource.import_data(dataset, dry_run=True)
        count=len(result.rows)
        if not result.has_errors():
            messages.info(request, 'Verify Information before saving into the database')
            return render(request, 'verify_theory_question_info.html', {'data': course_data, 'count': count, 'new_data': new_data})
        else:
            messages.error(request, 'There was an error importing the data')
                    
    return redirect('import-question')



def verify_data3(request):
    imported_data_json = request.session.get('imported_data', None)
    imported_course = request.session.get('imported_course', None)
    if not imported_data_json:
        return redirect('import-question')
    dataset = Dataset().load(imported_data_json)
    if request.method == 'POST':
        resource = TheoryQuestionFile()
        result = resource.import_data(dataset, dry_run=False)
        if not result.has_errors():
            cou = Course.objects.filter(name__in=imported_course)
            for cou in cou:
                cou.exam_control = False
                cou.control = False
                cou.save()
                question_values = [row[0] for row in dataset]
                for question in question_values:
                    que = Theory_Question.objects.get(question=question)
                    que.course.add(cou)
                    que.save()
            messages.success(request, 'Data imported successfully!')
        else:
            messages.error(request, 'There was an error importing the data')
    return redirect('import-question')
