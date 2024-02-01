from django import forms
from users.models import User, Department
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from exam.models import Course
        
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
    
    
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','department','duration','total_marks']
        


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','userid','department']      
