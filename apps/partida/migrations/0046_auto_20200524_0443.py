# Generated by Django 3.0.4 on 2020-05-24 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0045_auto_20200522_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-24 04:42:58', null=None),
        ),
    ]
