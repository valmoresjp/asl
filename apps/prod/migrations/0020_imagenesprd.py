# Generated by Django 3.0.4 on 2020-08-15 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0019_auto_20200729_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenesPRD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('imagen', models.ImageField(upload_to='imagenes/')),
            ],
        ),
    ]