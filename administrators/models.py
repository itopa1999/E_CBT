from django.db import models

# Create your models here.

class Access_Count(models.Model):
    count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-count']
        indexes = [
            models.Index(fields=['-count']),
        ]
        
    def __str__(self):
        return f"{self.count}"
    