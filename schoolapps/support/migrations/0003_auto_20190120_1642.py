# Generated by Django 2.1.5 on 2019-01-20 15:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('support', '0002_auto_20190120_1640'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='support',
            options={'permissions': (('use_rebus', 'Can use REBUS'), ('send_feedback', 'Can send feedback'))},
        ),
    ]
