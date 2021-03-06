# Generated by Django 3.0.4 on 2020-07-25 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0015_merge_20200724_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costosdescripcionm',
            name='umedida',
            field=models.CharField(choices=[('%', 'PORCENTAJE'), ('Kwh', 'KILOVATIO-HORA'), ('M3', 'METROS CUBICOS'), ('Lts', 'LITROS'), ('Kgr', 'KILOGRAMOS'), ('Gr', 'Gramos'), ('Mts', 'METROS'), ('Km', 'KILOMETROS'), ('Und', 'UNIDAD'), ('HH', 'HORAS-HOMBRE'), ('MES', 'MENUSAL'), ('DIA', 'DIARIO'), ('HRS', 'HORAS')], default='%', max_length=12),
        ),
    ]
