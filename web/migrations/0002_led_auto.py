# Generated by Django 2.2.4 on 2019-08-11 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='led',
            name='auto',
            field=models.BooleanField(default=False),
        ),
    ]