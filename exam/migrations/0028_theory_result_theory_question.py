# Generated by Django 4.2.7 on 2024-01-29 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0027_settings_delete_viewresult_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theory_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_marks', models.PositiveIntegerField(blank=True, null=True)),
                ('marks', models.PositiveIntegerField(blank=True, null=True)),
                ('missed_marks', models.PositiveIntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('time_used', models.DurationField(blank=True, null=True)),
                ('time_remaining', models.DurationField(blank=True, null=True)),
                ('file', models.FileField(upload_to='')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.course')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-end_time'],
                'indexes': [models.Index(fields=['-end_time'], name='exam_theory_end_tim_9939ae_idx')],
            },
        ),
        migrations.CreateModel(
            name='Theory_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('question', models.TextField(blank=True, max_length=1600, null=True, unique=True)),
                ('teacher_answer', models.TextField(blank=True, max_length=10000, null=True)),
                ('student_answer', models.TextField(blank=True, max_length=10000, null=True)),
                ('course', models.ManyToManyField(blank=True, to='exam.course')),
            ],
            options={
                'ordering': ['-question'],
                'indexes': [models.Index(fields=['-question'], name='exam_theory_questio_612e5d_idx')],
            },
        ),
    ]