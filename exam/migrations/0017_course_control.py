# Generated by Django 4.2.7 on 2024-01-17 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0016_alter_course_department_alter_question_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='control',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
