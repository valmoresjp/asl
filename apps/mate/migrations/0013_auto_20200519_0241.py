# Generated by Django 3.0.4 on 2020-05-19 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0012_auto_20200505_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtrosCostosM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descric', models.CharField(max_length=14)),
                ('umedida', models.FloatField(blank=True, default=0.0, null=True)),
                ('cantidad', models.FloatField(blank=True, default=0.0, null=True)),
                ('ctotal', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='insumosm',
            name='tipo',
            field=models.CharField(choices=[('MAT', 'MATERIAL'), ('PER', 'PERSONAL'), ('MYH', 'MAQyHERR'), ('SER', 'SERVICIO'), ('ING', 'INGREDIENTE')], default='ING', max_length=14),
        ),
    ]
