# Generated by Django 3.0.4 on 2020-07-19 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0102_auto_20200718_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-18 20:09:33', null=None),
        ),
    ]
