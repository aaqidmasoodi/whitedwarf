# Generated by Django 4.0.6 on 2022-09-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_first_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_coordinator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
    ]