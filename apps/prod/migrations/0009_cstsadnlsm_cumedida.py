# Generated by Django 3.0.4 on 2020-05-24 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0008_auto_20200524_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='cstsadnlsm',
            name='cumedida',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]