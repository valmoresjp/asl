# Generated by Django 3.0.4 on 2020-07-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0113_auto_20200721_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-21 16:14:10', null=None),
        ),
    ]
