# Generated by Django 2.0 on 2018-01-01 16:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('aub', '0010_auto_20180101_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aub',
            name='from_dt',
        ),
        migrations.RemoveField(
            model_name='aub',
            name='to_dt',
        ),
        migrations.AddField(
            model_name='aub',
            name='from_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='aub',
            name='from_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='aub',
            name='to_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='aub',
            name='to_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
