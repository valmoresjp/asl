# Generated by Django 3.0.4 on 2020-07-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_auto_20200719_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientesm',
            name='fhaniver',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
