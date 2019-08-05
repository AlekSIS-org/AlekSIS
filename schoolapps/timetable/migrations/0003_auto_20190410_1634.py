# Generated by Django 2.1.5 on 2019-04-10 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('timetable', '0002_hintclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='hint',
            name='classes',
            field=models.ManyToManyField(related_name='hints', to='timetable.HintClass'),
        ),
        migrations.AlterField(
            model_name='hintclass',
            name='class_id',
            field=models.IntegerField(
                choices=[(1, '5a'), (2, '5b'), (3, '5c'), (4, '5d'), (5, '6a'), (6, '6b'), (7, '6c'), (8, '6d'),
                         (9, '7a'), (10, '7b'), (11, '7c'), (12, '7d'), (13, '8a'), (14, '8b'), (15, '8c'), (16, '8d'),
                         (17, '9a'), (18, '9b'), (19, '9c'), (20, '9d'), (21, 'Ea'), (22, 'Eb'), (23, 'Ec'), (24, 'Ed'),
                         (25, 'Q1a'), (26, 'Q1b'), (27, 'Q1c'), (28, 'Q1d'), (29, 'Q2a'), (30, 'Q2b'), (31, 'Q2c'),
                         (32, 'Q2d')]),
        ),
    ]
