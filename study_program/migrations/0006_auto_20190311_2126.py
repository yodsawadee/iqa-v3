# Generated by Django 2.1.2 on 2019-03-11 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_program', '0005_auto_20190311_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabletime',
            name='appointment_date',
            field=models.DateField(default=datetime.datetime(2019, 3, 11, 21, 26, 25, 962616)),
        ),
        migrations.AlterField(
            model_name='availabletime',
            name='appointment_time',
            field=models.TimeField(default=datetime.datetime(2019, 3, 11, 21, 26, 25, 962616)),
        ),
    ]
