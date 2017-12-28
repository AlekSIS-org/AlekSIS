# Generated by Django 2.0 on 2017-12-22 16:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0004_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='to',
            field=models.ManyToManyField(related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
