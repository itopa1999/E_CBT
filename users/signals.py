from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User

'''@receiver(post_save, sender=User)
def send_job_notification(sender, instance, created, **kwargs):
    if not created:
        instance.set_password(instance.last_name.lower())'''