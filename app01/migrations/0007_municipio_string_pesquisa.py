# Generated by Django 4.0.1 on 2022-02-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_municipio_modelo'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipio',
            name='string_pesquisa',
            field=models.CharField(default='', max_length=100),
        ),
    ]