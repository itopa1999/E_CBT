from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
from .utils import *
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=150,unique=True, null=True,blank=True, default='')
    
    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    username = None
    userid = models.CharField(max_length=150, unique=True, null=True, blank=True)
    department =models.ForeignKey(Department,on_delete=models.SET_NULL,null=True, blank=True)
    login = models.BooleanField(default=False,null=True, blank=True)
    def save(self, *args, **kwargs):
        # If the user is being created and the password is not set, set a default password
        if not self.id and not self.password:
            self.set_password('pass1234')

        super().save(*args, **kwargs)

    objects=UserManager( )
    USERNAME_FIELD ='userid'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return f"{self.userid}"