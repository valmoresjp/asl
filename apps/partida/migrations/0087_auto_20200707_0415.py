# Generated by Django 3.0.4 on 2020-07-07 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0086_auto_20200707_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-07 04:15:54', null=None),
        ),
    ]
