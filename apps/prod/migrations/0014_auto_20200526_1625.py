# Generated by Django 3.0.4 on 2020-05-26 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0013_auto_20200526_1624'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cstsadnlsm',
            old_name='idprod',
            new_name='idprd',
        ),
    ]