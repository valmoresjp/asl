# Generated by Django 3.0.4 on 2020-09-19 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0025_auto_20200916_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenesm',
            name='img1',
            field=models.ImageField(default='Sin_Imagen_Seleccionada.png', upload_to='imagenes/'),
        ),
    ]
