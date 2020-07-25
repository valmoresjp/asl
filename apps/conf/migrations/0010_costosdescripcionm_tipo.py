# Generated by Django 3.0.4 on 2020-07-07 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0009_auto_20200707_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='costosdescripcionm',
            name='tipo',
            field=models.CharField(choices=[('SERV', 'SERVICIO'), ('MOBR', 'INSUMOS'), ('MYHR', 'MAQUINAS y HERRAMIENTAS'), ('GGEN', 'GASTOS GENERALES')], default='SERVICIO', max_length=4),
        ),
    ]
