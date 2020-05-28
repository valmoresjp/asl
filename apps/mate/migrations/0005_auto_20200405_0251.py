# Generated by Django 3.0.4 on 2020-04-05 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0004_auto_20200402_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumosm',
            name='cantm1',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='insumosm',
            name='cantm2',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AlterField(
            model_name='insumosm',
            name='cantm3',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AlterField(
            model_name='insumosm',
            name='cantm4',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AlterField(
            model_name='insumosm',
            name='cantm5',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
    ]
