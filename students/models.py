from django.db import models
from users.models import User
# Create your models here.

class ExamMode(models.Model):
    student = models.OneToOneField(User,on_delete=models.SET_NULL,null=True, blank=True)
    
    class Meta:
        ordering = ['-student']
        indexes = [
            models.Index(fields=['-student']),
        ]
        
    def __str__(self):
        return f"{self.student}"
    
    
class Submitted(models.Model):
    student = models.OneToOneField(User,on_delete=models.SET_NULL,null=True, blank=True)
    
    class Meta:
        ordering = ['-student']
        indexes = [
            models.Index(fields=['-student']),
        ]
    
    def __str__(self):
        return f"{self.student}"