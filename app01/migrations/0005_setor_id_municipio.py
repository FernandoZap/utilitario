# Generated by Django 4.0.1 on 2022-02-05 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_setor'),
    ]

    operations = [
        migrations.AddField(
            model_name='setor',
            name='id_municipio',
            field=models.IntegerField(default=0),
        ),
    ]
