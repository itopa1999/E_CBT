# Generated by Django 4.2.7 on 2024-03-08 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0033_settings_e_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
