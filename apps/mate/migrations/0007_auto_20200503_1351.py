# Generated by Django 3.0.4 on 2020-05-03 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0006_auto_20200405_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumosm',
            name='cmedi1',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='cmedi2',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='cmedi3',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='cmedi4',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='insumosm',
            name='cmedi5',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
    ]
