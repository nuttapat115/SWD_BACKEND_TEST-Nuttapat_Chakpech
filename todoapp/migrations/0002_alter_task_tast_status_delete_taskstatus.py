# Generated by Django 4.0.4 on 2023-02-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tast_status',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='TaskStatus',
        ),
    ]
