# Generated by Django 3.0.4 on 2020-04-29 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0006_auto_20200405_0322'),
        ('partida', '0020_auto_20200424_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=None, default='2020-04-29 13:36:56', null=None),
        ),
        migrations.AlterField(
            model_name='partidadetallesm',
            name='codi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mate.InsumosM'),
        ),
    ]
