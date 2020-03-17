# Generated by Django 3.0.2 on 2020-01-29 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0008_rename_fields_notification_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Widget Title')),
                ('active', models.BooleanField(blank=True, verbose_name='Activate Widget')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.dashboardwidget_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Dashboard Widget',
                'verbose_name_plural': 'Dashboard Widgets',
            },
        ),
    ]