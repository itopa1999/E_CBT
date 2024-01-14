from django.db import models
from users.models import User, Department
from django.utils import timezone

# Create your models here.


class Course(models.Model):
   name = models.CharField(max_length=150, unique=True,)
   department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True, blank=True)
   total_marks = models.PositiveIntegerField(null=True, blank = True)
   duration = models.PositiveIntegerField(null=True, blank=True)
   
   class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-name']),
        ]
   
   def __str__(self):
        return self.name
    

class Question(models.Model):
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True, blank=True)
    marks=models.PositiveIntegerField()
    question=models.TextField(max_length=1600,null=True, blank=True,unique=True,)
    option1=models.CharField(max_length=1000,null=True, blank=True)
    option2=models.CharField(max_length=1000,null=True, blank=True)
    option3=models.CharField(max_length=1000,null=True, blank=True)
    option4=models.CharField(max_length=1000,null=True, blank=True)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=1000,choices=cat,null=True, blank=True)
    
    class Meta:
        ordering = ['-course']
        indexes = [
            models.Index(fields=['-course']),
        ]
    
    def __str__(self):
        return f"{self.question}"
    
    
class Result(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    exam = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True, blank=True)
    total_marks = models.PositiveIntegerField(null=True, blank=True)
    marks = models.PositiveIntegerField(null=True, blank=True)
    missed_marks = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_used = models.DurationField(null=True, blank=True)
    time_remaining = models.DurationField(null=True, blank=True)
    

    class Meta:
        ordering = ['-end_time']
        indexes = [
            models.Index(fields=['-end_time']),
        ]
    
    def __str__(self):
        return f"{self.student} scores {self.marks}"