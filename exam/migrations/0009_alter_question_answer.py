# Generated by Django 4.2.7 on 2024-01-11 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_alter_question_answer_alter_question_option1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
