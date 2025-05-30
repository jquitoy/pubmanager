# Generated by Django 4.2.8 on 2025-05-26 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pub', '0002_rename_staff_id_roles_role_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('task_type', models.CharField(choices=[('OBS', 'Observance (Mandatory)'), ('COV', 'Coverage (Optional)')], max_length=3)),
                ('deadline', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('POSTED', 'Posted'), ('MISSED', 'Missed'), ('CANCELLED', 'Cancelled'), ('WORKING', 'Working')], default='WORKING', max_length=20)),
            ],
            options={
                'db_table': 'tbl_tasks',
            },
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined'), ('SUBMITTED', 'Submitted'), ('MISSED', 'Missed Deadline')], default='PENDING', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pub.staffs')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pub.tasks')),
            ],
        ),
    ]
