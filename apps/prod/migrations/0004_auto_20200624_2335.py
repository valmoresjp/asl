# Generated by Django 3.0.4 on 2020-06-24 23:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0003_auto_20200618_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosm',
            name='fhactu',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='productosm',
            name='fhcrea',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productosm',
            name='fhentr',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
