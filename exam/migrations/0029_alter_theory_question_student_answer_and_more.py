# Generated by Django 4.2.7 on 2024-01-29 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0028_theory_result_theory_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theory_question',
            name='student_answer',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='theory_question',
            name='teacher_answer',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
