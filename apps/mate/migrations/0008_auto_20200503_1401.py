# Generated by Django 3.0.4 on 2020-05-03 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0007_auto_20200503_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumosm',
            name='cmedi1',
        ),
        migrations.RemoveField(
            model_name='insumosm',
            name='cmedi2',
        ),
        migrations.RemoveField(
            model_name='insumosm',
            name='cmedi3',
        ),
        migrations.RemoveField(
            model_name='insumosm',
            name='cmedi4',
        ),
        migrations.RemoveField(
            model_name='insumosm',
            name='cmedi5',
        ),
    ]
