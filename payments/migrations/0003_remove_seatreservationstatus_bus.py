# Generated by Django 4.0.6 on 2022-09-09 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_seatreservationstatus_delete_seatreservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatreservationstatus',
            name='bus',
        ),
    ]
