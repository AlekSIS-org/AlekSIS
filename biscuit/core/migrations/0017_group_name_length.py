# Generated by Django 2.2.4 on 2019-09-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_parent_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=60, verbose_name='Long name of group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='short_name',
            field=models.CharField(max_length=16, verbose_name='Short name of group'),
        ),
    ]
