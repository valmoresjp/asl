# Generated by Django 3.0.4 on 2020-10-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0152_auto_20201011_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-11 11:33:31', null=None),
        ),
    ]
