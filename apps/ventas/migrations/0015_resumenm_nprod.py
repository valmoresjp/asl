# Generated by Django 3.0.4 on 2020-10-30 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0014_auto_20200929_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumenm',
            name='nprod',
            field=models.IntegerField(default=0),
        ),
    ]
