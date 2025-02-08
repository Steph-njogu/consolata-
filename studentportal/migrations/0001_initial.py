# Generated by Django 5.1.4 on 2025-02-08 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admission', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/pdfs/')),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('title', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.admissionstudent')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.campus')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='course.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.department')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='course.field')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.admissionstudent')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.yearofstudy')),
            ],
            options={
                'indexes': [models.Index(fields=['student', 'course', 'semester'], name='studentport_student_548c43_idx')],
                'unique_together': {('student', 'course')},
            },
        ),
    ]
