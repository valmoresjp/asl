# Generated by Django 3.0.4 on 2020-06-18 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0002_auto_20200618_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productosm',
            old_name='costo1',
            new_name='costo',
        ),
    ]
