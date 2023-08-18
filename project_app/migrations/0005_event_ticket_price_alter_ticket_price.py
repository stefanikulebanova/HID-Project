# Generated by Django 4.2.4 on 2023-08-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0004_ticket_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
