# Generated by Django 3.0.5 on 2020-04-30 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('core', '0024_globalpermissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPreferenceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(blank=True, db_index=True, default=None, max_length=150, null=True, verbose_name='Section Name')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Name')),
                ('raw_value', models.TextField(blank=True, null=True, verbose_name='Raw Value')),
            ],
        ),
        migrations.CreateModel(
            name='PersonPreferenceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(blank=True, db_index=True, default=None, max_length=150, null=True, verbose_name='Section Name')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Name')),
                ('raw_value', models.TextField(blank=True, null=True, verbose_name='Raw Value')),
            ],
        ),
        migrations.CreateModel(
            name='SitePreferenceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(blank=True, db_index=True, default=None, max_length=150, null=True, verbose_name='Section Name')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='Name')),
                ('raw_value', models.TextField(blank=True, null=True, verbose_name='Raw Value')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
        migrations.DeleteModel(
            name='School',
        ),
        migrations.DeleteModel(
            name='SchoolTerm',
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['short_name', 'name'], 'permissions': (('assign_child_groups_to_groups', 'Can assign child groups to groups'),), 'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('view_address', 'Can view address'), ('view_contact_details', 'Can view contact details'), ('view_photo', 'Can view photo'), ('view_person_groups', 'Can view persons groups'), ('view_personal_details', 'Can view personal details')), 'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AddField(
            model_name='personpreferencemodel',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Person'),
        ),
        migrations.AddField(
            model_name='grouppreferencemodel',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Group'),
        ),
    ]
