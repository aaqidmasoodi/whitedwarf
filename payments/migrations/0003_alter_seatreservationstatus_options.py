# Generated by Django 4.0.6 on 2022-09-13 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_bus_alter_payment_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seatreservationstatus',
            options={'verbose_name_plural': 'Seat Reservation Statuses'},
        ),
    ]