from django import forms
from users.models import User, Department
from .models import *

        
        
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']