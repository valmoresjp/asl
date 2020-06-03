# Generated by Django 3.0.4 on 2020-05-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0006_auto_20200531_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costosdescripcionm',
            name='referencia',
            field=models.CharField(choices=[('UMED', 'UNIDAD/MEDIDA'), ('TINS', 'INSUMOS'), ('TMAT', 'MATERIALES'), ('TIMA', 'INSUMOS+MATERIALES')], default='INSUMOS+MATERIALES', max_length=10),
        ),
        migrations.AlterField(
            model_name='costosdescripcionm',
            name='umedida',
            field=models.CharField(choices=[('%', 'PORCENTAJE'), ('Kwh', 'KILOVATIO-HORA'), ('M3', 'METROS CUBICOS'), ('Lts', 'LITROS'), ('Kgr', 'KILOGRAMOS'), ('Gr', 'Gramos'), ('Mts', 'METROS'), ('Km', 'KILOMETROS'), ('Und', 'UNIDAD')], default='%', max_length=12),
        ),
    ]
