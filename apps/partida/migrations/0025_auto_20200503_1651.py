# Generated by Django 3.0.4 on 2020-05-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0024_auto_20200503_1401'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CostoPartida',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-03 16:51:37', null=None),
        ),
    ]
