# Generated by Django 3.0.4 on 2020-05-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0060_auto_20200528_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-05-28 21:48:50', null=None),
        ),
    ]