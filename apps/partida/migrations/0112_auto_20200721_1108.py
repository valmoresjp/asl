# Generated by Django 3.0.4 on 2020-07-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0111_auto_20200720_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-21 11:08:15', null=None),
        ),
    ]
