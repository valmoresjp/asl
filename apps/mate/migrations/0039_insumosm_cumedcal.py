# Generated by Django 3.0.4 on 2020-10-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0038_auto_20201013_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumosm',
            name='cumedcal',
            field=models.FloatField(default=1.0),
        ),
    ]
