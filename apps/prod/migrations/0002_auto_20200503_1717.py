# Generated by Django 3.0.4 on 2020-05-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productosm',
            name='codp',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='productosm',
            name='nomb',
            field=models.CharField(max_length=40),
        ),
    ]
