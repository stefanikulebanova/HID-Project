# Generated by Django 4.2.1 on 2023-08-21 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0007_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, upload_to='posts'),
        ),
    ]