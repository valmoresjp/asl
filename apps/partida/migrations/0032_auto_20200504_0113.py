# Generated by Django 3.0.4 on 2020-05-04 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0031_auto_20200504_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-04 01:13:36', null=None),
        ),
    ]
