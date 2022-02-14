# Generated by Django 4.0.1 on 2022-02-13 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0050_delete_folha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folha',
            fields=[
                ('id_folha', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('anomes', models.IntegerField()),
                ('id_funcionario', models.IntegerField()),
                ('id_departamento', models.IntegerField()),
                ('id_setor', models.IntegerField()),
                ('id_cargo', models.IntegerField()),
                ('id_vinculo', models.IntegerField()),
                ('id_provento', models.IntegerField()),
                ('tipo', models.CharField(max_length=1)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=9)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'folha',
            },
        ),
    ]