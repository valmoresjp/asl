# Generated by Django 3.0.4 on 2020-11-06 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0164_auto_20201031_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-11-06 00:47:30', null=None),
        ),
    ]
