# Generated by Django 3.0.4 on 2020-05-26 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0012_auto_20200526_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cstsadnlsm',
            old_name='idprd',
            new_name='idprod',
        ),
    ]