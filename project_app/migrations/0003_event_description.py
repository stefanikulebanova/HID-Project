# Generated by Django 4.2.4 on 2023-08-14 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0002_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='Description for event. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididu ut labore et dolore magna aliqua... ', max_length=300),
        ),
    ]
