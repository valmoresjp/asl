# Generated by Django 3.0.4 on 2020-05-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0037_auto_20200505_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-05 17:19:41', null=None),
        ),
    ]
