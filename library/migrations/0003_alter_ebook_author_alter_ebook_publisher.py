# Generated by Django 5.1.4 on 2025-02-09 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_remove_ebookbookmark_ebook_remove_ebookbookmark_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.author'),
        ),
        migrations.AlterField(
            model_name='ebook',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.publisher'),
        ),
    ]
