# Generated by Django 4.0.4 on 2023-02-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_alter_task_tast_status_delete_taskstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
