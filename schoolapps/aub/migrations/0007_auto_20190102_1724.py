# Generated by Django 2.1.4 on 2019-01-02 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aub', '0006_merge_20190102_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aub',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='aub',
            name='status',
        ),
    ]
