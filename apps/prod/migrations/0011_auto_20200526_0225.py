# Generated by Django 3.0.4 on 2020-05-26 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0010_auto_20200524_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquiyherram',
            name='cant',
            field=models.FloatField(default=1.0),
        ),
    ]