# Generated by Django 3.0.4 on 2020-07-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0008_resumenm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventasm',
            name='estado',
            field=models.IntegerField(default=0),
        ),
    ]
