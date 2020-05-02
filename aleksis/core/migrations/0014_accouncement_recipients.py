# Generated by Django 3.0.3 on 2020-03-11 18:43

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models

import aleksis.core.models


class Migration(migrations.Migration):

     dependencies = [
         ('contenttypes', '0002_remove_content_type_name'),
         ('core', '0013_extensible_model_as_default'),
     ]

     operations = [
         migrations.AlterModelOptions(
            name='announcement',
            options={'verbose_name': 'Announcement', 'verbose_name_plural': 'Announcements'},
         ),
         migrations.RemoveField(
             model_name='announcement',
             name='content_type',
         ),
         migrations.RemoveField(
             model_name='announcement',
             name='recipient_id',
         ),
         migrations.AlterField(
             model_name='announcement',
             name='description',
             field=models.TextField(blank=True, max_length=500, verbose_name='Description'),
         ),
         migrations.AlterField(
             model_name='announcement',
             name='valid_until',
             field=models.DateTimeField(default=aleksis.core.util.core_helpers.now_tomorrow, verbose_name='Date and time until when to show'),
         ),
         migrations.CreateModel(
             name='AnnouncementRecipient',
             fields=[
                 ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                 ('recipient_id', models.PositiveIntegerField()),
                 ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='core.Announcement')),
                 ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
             ],
         ),
         migrations.AlterModelOptions(
             name='announcementrecipient',
             options={'verbose_name': 'Announcement recipient', 'verbose_name_plural': 'Announcement recipients'},
         ),
         migrations.AddField(
             model_name='announcementrecipient',
             name='extended_data',
             field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, editable=False),
         ),
     ]
