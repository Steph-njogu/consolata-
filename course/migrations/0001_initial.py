# Generated by Django 5.1.4 on 2025-02-08 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', models.CharField(choices=[('Main', 'Main campus'), ('Kirinyaga', 'Kirinyaga campus'), ('Kisumu', 'Kisumu campus')], default='Main', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=300)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('Semester1', 'Semester 1'), ('Semester2', 'Semester 2')], default='Semester1', max_length=30)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='course.campus')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='course.field')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='course.semester'),
        ),
        migrations.AddField(
            model_name='campus',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campuses', to='course.university'),
        ),
        migrations.CreateModel(
            name='YearOfStudy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('Year1', 'Year 1'), ('Year2', 'Year 2'), ('Year3', 'Year 3'), ('Year4', 'Year 4')], default='Year1', max_length=20, verbose_name='Year of Study')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='year_of_study', to='course.department')),
            ],
            options={
                'verbose_name': 'Year of Study',
                'verbose_name_plural': 'Years of Study',
            },
        ),
        migrations.AddField(
            model_name='semester',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='course.yearofstudy'),
        ),
    ]
