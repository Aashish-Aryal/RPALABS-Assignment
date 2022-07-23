# Generated by Django 3.2 on 2022-07-21 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('video', models.FileField(upload_to='videos')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]