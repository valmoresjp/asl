# Generated by Django 3.0.4 on 2020-05-04 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0030_auto_20200504_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-04 00:59:05', null=None),
        ),
    ]
