# Generated by Django 3.0.4 on 2020-10-30 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0015_resumenm_nprod'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resumenm',
            old_name='nprod',
            new_name='nprdv',
        ),
    ]
