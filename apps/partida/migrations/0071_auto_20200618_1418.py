# Generated by Django 3.0.4 on 2020-06-18 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0070_auto_20200618_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-06-18 14:18:13', null=None),
        ),
    ]
