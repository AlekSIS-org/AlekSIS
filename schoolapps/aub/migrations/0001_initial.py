# Generated by Django 2.2.1 on 2019-05-29 15:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('from_date', models.DateField(default=datetime.date.today, verbose_name='Startdatum')),
                ('from_time', models.TimeField(default=django.utils.timezone.now, verbose_name='Startzeit')),
                ('to_date', models.DateField(default=datetime.date.today, verbose_name='Enddatum')),
                ('to_time', models.TimeField(default=django.utils.timezone.now, verbose_name='Endzeit')),
                ('description', models.TextField()),
                ('status', models.IntegerField(
                    choices=[(0, 'In Bearbeitung 1'), (1, 'In Bearbeitung 2'), (2, 'Genehmigt'), (3, 'Abgelehnt')],
                    default=0, verbose_name='Status')),
                ('created_at',
                 models.DateTimeField(default=django.utils.timezone.now, verbose_name='Erstellungszeitpunkt')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 related_name='aubs', to=settings.AUTH_USER_MODEL,
                                                 verbose_name='Erstellt von')),
            ],
            options={
                'verbose_name': 'AUB',
                'verbose_name_plural': 'AUBs',
                'permissions': (('apply_for_aub', 'Apply for a AUB'), ('cancel_aub', 'Cancel a AUB'),
                                ('allow1_aub', 'First permission'), ('allow2_aub', 'Second permission'),
                                ('check1_aub', 'Check a AUB'), ('check2_aub', 'Check a AUB'),
                                ('view_archive', 'View AUB archive')),
            },
        ),
    ]
