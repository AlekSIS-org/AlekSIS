# Generated by Django 2.0 on 2017-12-20 19:26

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default=datetime.datetime(2017, 12, 20, 20, 26, 25, 530658))),
                ('to_date', models.DateField(default=datetime.datetime(2017, 12, 20, 20, 26, 25, 530704))),
                ('from_lesson',
                 models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)],
                                     default=1)),
                ('to_lesson',
                 models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)],
                                     default=1)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 12, 20, 20, 26, 25, 614555))),
                ('created_by', models.ForeignKey(default=None, on_delete=models.SET(None), related_name='aubs',
                                                 to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
