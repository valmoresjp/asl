# Generated by Django 3.0.4 on 2020-10-15 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0160_auto_20201014_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-15 01:29:26', null=None),
        ),
    ]