# Generated by Django 3.2.25 on 2025-02-05 23:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_auto_20250205_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(default=datetime.time(23, 41, 46, 588567)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(default=datetime.time(23, 41, 46, 588552)),
        ),
    ]
