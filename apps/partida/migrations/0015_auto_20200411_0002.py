# Generated by Django 3.0.4 on 2020-04-11 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0014_auto_20200406_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-04-11 00:02:58', null=None),
        ),
    ]
