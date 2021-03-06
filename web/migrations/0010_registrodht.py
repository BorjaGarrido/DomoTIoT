# Generated by Django 2.2.4 on 2019-08-15 17:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20190814_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='registroDHT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperaturaMax', models.FloatField(default=0, null=True)),
                ('humedadMax', models.FloatField(default=0, null=True)),
                ('fechaTMax', models.DateField(default=django.utils.timezone.now)),
                ('fechaHMax', models.DateField(default=django.utils.timezone.now)),
                ('horaTMax', models.TimeField(default=django.utils.timezone.now)),
                ('horaHMax', models.TimeField(default=django.utils.timezone.now)),
                ('temperaturaMin', models.FloatField(default=100, null=True)),
                ('humedadMin', models.FloatField(default=100, null=True)),
                ('fechaTMin', models.DateField(default=django.utils.timezone.now)),
                ('fechaHMin', models.DateField(default=django.utils.timezone.now)),
                ('horaTMin', models.TimeField(default=django.utils.timezone.now)),
                ('horaHMin', models.TimeField(default=django.utils.timezone.now)),
                ('dht', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.dht')),
            ],
        ),
    ]
