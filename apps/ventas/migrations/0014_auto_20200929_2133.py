# Generated by Django 3.0.4 on 2020-09-30 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0013_auto_20200929_2120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resumenm',
            old_name='ncli',
            new_name='ncli_a',
        ),
        migrations.AddField(
            model_name='resumenm',
            name='ncli_n',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resumenm',
            name='ncli_t',
            field=models.IntegerField(default=0),
        ),
    ]