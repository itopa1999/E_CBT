# Generated by Django 4.2.7 on 2024-01-29 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0030_alter_theory_question_student_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theory_result',
            name='file',
        ),
        migrations.CreateModel(
            name='Theory_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.course')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-student'],
                'indexes': [models.Index(fields=['-student'], name='exam_theory_student_16b44b_idx')],
            },
        ),
    ]
