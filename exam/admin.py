from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Course)
admin.site.register(Result)
admin.site.register(Question)
admin.site.register(Theory_Result)
admin.site.register(Theory_Question)
admin.site.register(School_Info)
admin.site.register(Theory_File)