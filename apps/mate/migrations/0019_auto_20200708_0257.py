# Generated by Django 3.0.4 on 2020-07-08 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0018_remove_insumosm_fingso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumosm',
            name='tipo',
            field=models.CharField(max_length=4),
        ),
    ]