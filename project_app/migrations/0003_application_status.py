# Generated by Django 4.2.4 on 2023-08-16 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0002_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(default='Waiting', max_length=150),
        ),
    ]
