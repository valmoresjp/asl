# Generated by Django 3.0.4 on 2020-06-29 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0084_auto_20200629_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-06-29 15:54:48', null=None),
        ),
    ]