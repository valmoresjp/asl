# Generated by Django 3.0.4 on 2020-04-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0002_auto_20200331_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumosm',
            name='ctmax',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='ctmin',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='ctprom',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
