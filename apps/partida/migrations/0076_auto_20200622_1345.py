# Generated by Django 3.0.4 on 2020-06-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0075_auto_20200618_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-06-22 13:45:16', null=None),
        ),
    ]
