# Generated by Django 3.0.4 on 2020-05-26 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0051_auto_20200524_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-26 02:25:31', null=None),
        ),
        migrations.AlterField(
            model_name='partidasm',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
    ]
