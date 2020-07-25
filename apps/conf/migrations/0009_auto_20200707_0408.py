# Generated by Django 3.0.4 on 2020-07-07 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0008_auto_20200614_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costosdescripcionm',
            name='referencia',
            field=models.CharField(choices=[('UMED', 'UNIDAD/MEDIDA'), ('TINS', 'INSUMOS'), ('TMAT', 'MATERIALES'), ('MOBR', 'MANO DE OBRA'), ('TCAD', 'COSTOS_ADICIONALES'), ('TIMA', 'INSUMOS+MATERIALES'), ('IMAC', 'INSUMOS+MATERIALES+COSTOS_ADICIONALES'), ('IMACM', 'INSUMOS+MATERIALES+COSTOS_ADICIONALES+MANO_OBRA')], default='INSUMOS+MATERIALES', max_length=10),
        ),
    ]
