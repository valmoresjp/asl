# Generated by Django 3.0.4 on 2020-10-14 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0158_auto_20201013_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-10-13 23:18:30', null=None),
        ),
    ]