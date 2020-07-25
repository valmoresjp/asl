# Generated by Django 3.0.4 on 2020-06-29 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0006_auto_20200626_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosm',
            name='cadln',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productosm',
            name='insm',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productosm',
            name='mate',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productosm',
            name='mobra',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productosm',
            name='utlds',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]