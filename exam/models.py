from django.db import models
from users.models import User, Department, Level
from django.utils import timezone

# Create your models here.


class Course(models.Model):
   name = models.CharField(max_length=150, unique=True,)
   department = models.ManyToManyField(Department, blank=True)
   total_marks = models.PositiveIntegerField(null=True, blank = True)
   duration = models.PositiveIntegerField(null=True, blank=True)
   control = models.BooleanField(default=False, null=True, blank=True)
   exam_control = models.BooleanField(default=True, null=True, blank=True)
   
   
   class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-name']),
        ]
   
   def __str__(self):
        return self.name
    

class Question(models.Model):
    course = models.ManyToManyField(Course,blank=True)
    marks=models.PositiveIntegerField()
    question=models.TextField(max_length=160000,null=True, blank=True)
    A=models.CharField(max_length=10000,null=True, blank=True)
    B=models.CharField(max_length=100000,null=True, blank=True)
    C=models.CharField(max_length=100000,null=True, blank=True)
    D=models.CharField(max_length=100000,null=True, blank=True)
    answer=models.CharField(max_length=1000,null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.answer = (self.answer.strip()).upper()
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['-question']
        indexes = [
            models.Index(fields=['-question']),
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
    


class Theory_Question(models.Model):
    course = models.ManyToManyField(Course,blank=True)
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    marks=models.PositiveIntegerField()
    question=models.TextField(max_length=1600,null=True, blank=True,unique=True)
    teacher_answer=models.TextField(max_length=10000,null=True, blank=True)
    student_answer=models.TextField(max_length=10000,null=True, blank=True)
    
    
    
    '''def save(self, *args, **kwargs):
        self.teacher_answer = self.teacher_answer.lower()
        self.student_answer = self.student_answer.lower()
        super().save(*args, **kwargs)'''
    class Meta:
        ordering = ['-question']
        indexes = [
            models.Index(fields=['-question']),
        ]
    
    def __str__(self):
        return f"{self.question}"



class Theory_Result(models.Model):
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



class Theory_File(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    exam = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True, blank=True)
    file = models.FileField()
    
    class Meta:
        ordering = ['-student']
        indexes = [
            models.Index(fields=['-student']),
        ]
    
    def __str__(self):
        return f"{self.student}"



class Settings(models.Model):
    view_result = models.BooleanField(default=False, null=True, blank=True)
    stop_time = models.BooleanField(default=False, null=True, blank=True)
    e_pin = models.BooleanField(default=False, null=True, blank=True)
    class Meta:
        ordering = ['-view_result']
        indexes = [
            models.Index(fields=['-view_result']),
        ]
    


class School_Info(models.Model):
    name = models.CharField(max_length=10000,null=True, blank=True)
    address = models.CharField(max_length=10000,null=True, blank=True)
    semester = models.CharField(max_length=10000,null=True, blank=True)
    
    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-name']),
        ]
    
    