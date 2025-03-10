# Generated by Django 5.1.4 on 2025-01-29 12:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminary', '0007_alter_profile_user_alter_roomassignment_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seminarian', to=settings.AUTH_USER_MODEL),
        ),
    ]
