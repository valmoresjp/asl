# Generated by Django 3.0.4 on 2020-06-25 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0079_auto_20200624_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-06-25 01:35:17', null=None),
        ),
    ]
