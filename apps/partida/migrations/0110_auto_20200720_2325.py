# Generated by Django 3.0.4 on 2020-07-21 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0109_auto_20200720_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-20 23:25:33', null=None),
        ),
    ]
