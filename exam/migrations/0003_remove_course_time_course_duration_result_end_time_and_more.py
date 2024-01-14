# Generated by Django 4.2.7 on 2024-01-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_course_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='time',
        ),
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
