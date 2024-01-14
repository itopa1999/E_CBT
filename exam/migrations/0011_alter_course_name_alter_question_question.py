# Generated by Django 4.2.7 on 2024-01-11 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_alter_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(blank=True, max_length=1600, null=True, unique=True),
        ),
    ]
