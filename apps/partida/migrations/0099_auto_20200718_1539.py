# Generated by Django 3.0.4 on 2020-07-18 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0098_auto_20200718_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-18 15:39:11', null=None),
        ),
    ]