# Generated by Django 3.0.4 on 2020-07-19 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0104_auto_20200718_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-18 20:13:49', null=None),
        ),
    ]