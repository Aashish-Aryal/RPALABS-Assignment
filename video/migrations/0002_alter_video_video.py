# Generated by Django 3.2 on 2022-07-21 01:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='videos', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mkv'])]),
        ),
    ]
