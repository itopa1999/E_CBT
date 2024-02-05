from django.db import models
from users.models import User
# Create your models here.

class E_PinManager(models.Manager):
    def unassigned_and_unused_pins(self):
        return self.filter(student__isnull=True, used=False, expired=False)


class Access_Count(models.Model):
    count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-count']
        indexes = [
            models.Index(fields=['-count']),
        ]
        
    def __str__(self):
        return f"{self.count}"



class E_Pin(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    pin = models.CharField(max_length=15)
    used = models.BooleanField(default=False,blank=True)
    expired = models.BooleanField(default=False,blank=True)
    
    
    objects = E_PinManager()
    
    class Meta:
        ordering = ['-used']
        indexes = [
            models.Index(fields=['-used']),
        ]
        
    def __str__(self):
        return f"{self.student}"