# Generated by Django 5.2.3 on 2025-07-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterstudent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterstudent',
            name='photo_path',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
