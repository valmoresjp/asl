# Generated by Django 3.0.4 on 2020-05-30 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0016_auto_20200530_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productosm',
            name='costo',
            field=models.FloatField(default=0.0),
        ),
    ]
