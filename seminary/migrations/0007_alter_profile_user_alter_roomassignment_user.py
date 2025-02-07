# Generated by Django 5.1.4 on 2025-01-28 22:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminary', '0006_alter_roomassignment_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seminiarian', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='roomassignment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='room_assignments', to=settings.AUTH_USER_MODEL),
        ),
    ]
