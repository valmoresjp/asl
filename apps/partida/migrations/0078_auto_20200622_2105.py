# Generated by Django 3.0.4 on 2020-06-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0077_auto_20200622_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-06-22 21:05:26', null=None),
        ),
    ]
