# Generated by Django 3.0.4 on 2020-10-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0148_auto_20201005_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-05 12:12:40', null=None),
        ),
    ]
