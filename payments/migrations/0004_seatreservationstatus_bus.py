# Generated by Django 4.0.6 on 2022-09-10 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0001_initial'),
        ('payments', '0003_remove_seatreservationstatus_bus'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatreservationstatus',
            name='bus',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buses.bus'),
        ),
    ]
