# Generated by Django 3.0.4 on 2020-04-06 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0012_auto_20200405_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-04-06 01:21:03', null=None),
        ),
    ]
