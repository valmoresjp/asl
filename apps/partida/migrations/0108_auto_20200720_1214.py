# Generated by Django 3.0.4 on 2020-07-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0107_auto_20200719_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-20 12:14:15', null=None),
        ),
    ]
