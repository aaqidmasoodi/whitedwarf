# Generated by Django 4.0.6 on 2022-08-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentvalidationtoken',
            name='token',
            field=models.CharField(max_length=600),
        ),
    ]
