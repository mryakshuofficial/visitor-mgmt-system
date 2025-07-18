# Generated by Django 5.2.3 on 2025-07-18 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gr_no', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('student_class', models.CharField(blank=True, max_length=20, null=True)),
                ('fname', models.CharField(blank=True, max_length=100, null=True)),
                ('lname', models.CharField(blank=True, max_length=100, null=True)),
                ('surname', models.CharField(blank=True, max_length=100, null=True)),
                ('village', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('aadhar', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('photo_path', models.ImageField(blank=True, null=True, upload_to='student_photos/')),
            ],
        ),
    ]
