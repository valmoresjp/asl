# Generated by Django 3.0.4 on 2020-10-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0147_auto_20200929_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-05 10:20:17', null=None),
        ),
    ]
