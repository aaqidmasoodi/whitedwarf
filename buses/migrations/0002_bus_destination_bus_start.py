# Generated by Django 4.0.6 on 2022-08-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='destination',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='start',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]