from django.contrib import admin
from .models import User, Department,Level

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("userid","first_name","last_name" ,"department")

admin.site.register(User, UserAdmin)

admin.site.register(Department)

admin.site.register(Level)