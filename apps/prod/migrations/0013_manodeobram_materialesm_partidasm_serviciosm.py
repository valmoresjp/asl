# Generated by Django 3.0.4 on 2020-07-18 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0012_auto_20200718_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManoDeObraM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('idmobra', models.IntegerField()),
                ('cumedida', models.FloatField(default=1.0)),
                ('cant', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialesM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('idmate', models.IntegerField()),
                ('cumedida', models.FloatField(default=1.0)),
                ('cant', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='PartidasM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('idpart', models.IntegerField()),
                ('unid', models.CharField(max_length=10)),
                ('cant', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('idserv', models.IntegerField()),
                ('cumedida', models.FloatField(default=1.0)),
                ('cant', models.FloatField(default=0.0)),
            ],
        ),
    ]
