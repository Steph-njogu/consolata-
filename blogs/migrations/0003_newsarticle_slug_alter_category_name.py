# Generated by Django 5.1.4 on 2025-01-31 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_newsarticle_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
    ]
