# Generated by Django 3.0.4 on 2020-05-30 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0059_auto_20200529_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-30 02:41:08', null=None),
        ),
    ]
