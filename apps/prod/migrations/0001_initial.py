from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CstsAdnlsM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcstanls', models.IntegerField()),
                ('idprd', models.IntegerField()),
                ('cumedida', models.FloatField(default=1.0)),
                ('cant', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='MaquiyHerraM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idism', models.IntegerField()),
                ('idprd', models.IntegerField()),
                ('unid', models.CharField(max_length=4)),
                ('cant', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductosDetallesM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idprd', models.IntegerField()),
                ('idpart', models.IntegerField()),
                ('unid', models.CharField(max_length=10)),
                ('cant', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductosM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomb', models.CharField(max_length=40)),
                ('codp', models.CharField(max_length=20)),
                ('desc', models.CharField(max_length=1000)),
                ('unid', models.CharField(max_length=10)),
                ('costo', models.FloatField(default=0.0)),
            ],
        ),
    ]
