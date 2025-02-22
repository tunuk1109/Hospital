# Generated by Django 5.1.6 on 2025-02-20 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0004_alter_feedback_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('person', models.ManyToManyField(to='hospital_app.doctorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.patientprofile')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.chat')),
            ],
        ),
    ]
