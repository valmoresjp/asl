# Generated by Django 3.0.4 on 2020-11-01 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0163_auto_20201029_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-31 22:04:50', null=None),
        ),
    ]
