# Generated by Django 4.2.7 on 2024-03-10 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0034_alter_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='A',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='B',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='C',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='D',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(blank=True, max_length=160000, null=True),
        ),
    ]
