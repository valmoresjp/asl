# Generated by Django 3.0.4 on 2020-04-24 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0018_auto_20200412_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-04-24 04:45:50', null=None),
        ),
    ]
