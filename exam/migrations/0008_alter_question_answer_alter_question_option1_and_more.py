# Generated by Django 4.2.7 on 2024-01-11 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_alter_question_answer_alter_question_option1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(blank=True, choices=[('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4')], max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option3',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='option4',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(blank=True, max_length=1600, null=True),
        ),
    ]
