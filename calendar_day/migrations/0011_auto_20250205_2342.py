# Generated by Django 3.2.25 on 2025-02-05 23:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_day', '0010_auto_20250205_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarblock',
            name='end_time',
            field=models.TimeField(default=datetime.time(23, 42, 49, 72328)),
        ),
        migrations.AlterField(
            model_name='calendarblock',
            name='start_time',
            field=models.TimeField(default=datetime.time(23, 42, 49, 72317)),
        ),
    ]
