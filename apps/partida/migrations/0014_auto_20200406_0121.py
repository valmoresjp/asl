# Generated by Django 3.0.4 on 2020-04-06 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0013_auto_20200406_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-04-06 01:21:16', null=None),
        ),
    ]
