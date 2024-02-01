from django.db.models.signals import post_save
from users.models import Level, Department
from django.dispatch import receiver


'''@receiver(post_save, sender=Department)
def create_department(sender, instance, created, **kwargs):
    if created:
        for i in range(3):
            random_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            Department.objects.create(name=random_name, level=None)
            if i == 3:
                break
'''