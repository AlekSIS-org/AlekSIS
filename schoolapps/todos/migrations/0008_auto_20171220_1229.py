# Generated by Django 2.0 on 2017-12-20 11:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0007_auto_20171219_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 20, 12, 28, 31, 666739)),
        ),
    ]
