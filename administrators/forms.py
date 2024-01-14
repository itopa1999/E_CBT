from django import forms
from users.models import User, Department
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm

        
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
    
    
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['department']