# Generated by Django 3.0.4 on 2020-07-18 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partida', '0095_auto_20200718_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-07-18 01:16:14', null=None),
        ),
    ]