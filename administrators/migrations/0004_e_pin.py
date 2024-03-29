# Generated by Django 4.2.7 on 2024-02-04 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrators', '0003_alter_access_count_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='E_Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=15)),
                ('used', models.BooleanField(blank=True, default=False)),
                ('expired', models.BooleanField(blank=True, default=False)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['used'],
                'indexes': [models.Index(fields=['used'], name='administrat_used_733f4a_idx')],
            },
        ),
    ]
