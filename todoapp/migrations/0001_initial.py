# Generated by Django 4.0.4 on 2023-02-23 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StepOfTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_text', models.TextField(max_length=255)),
                ('state_step', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=255)),
                ('task_description', models.TextField(max_length=255)),
                ('due_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTagGruop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.tag')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.task')),
            ],
        ),
        migrations.AddConstraint(
            model_name='taskstatus',
            constraint=models.UniqueConstraint(fields=('status_name',), name='unique_status_name'),
        ),
        migrations.AddField(
            model_name='task',
            name='tast_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='todoapp.taskstatus'),
        ),
        migrations.AddField(
            model_name='stepoftask',
            name='task_own',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.task'),
        ),
    ]
