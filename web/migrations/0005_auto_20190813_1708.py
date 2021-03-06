# Generated by Django 2.2.4 on 2019-08-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_led_nivelprogramado'),
    ]

    operations = [
        migrations.AddField(
            model_name='led',
            name='autoProgramado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='led',
            name='nivelProgramado',
            field=models.CharField(choices=[('Baja', 124), ('Media', 512), ('Máxima', 1024)], default=None, max_length=50),
        ),
    ]
