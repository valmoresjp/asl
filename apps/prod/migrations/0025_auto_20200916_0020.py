# Generated by Django 3.0.4 on 2020-09-16 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0024_auto_20200902_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenesm',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
        migrations.AlterField(
            model_name='imagenesm',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
        migrations.AlterField(
            model_name='imagenesm',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
        migrations.AlterField(
            model_name='imagenesm',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]