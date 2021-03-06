# Generated by Django 4.0.1 on 2022-02-06 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0021_departamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_funcionario', models.IntegerField()),
                ('id_repartition', models.IntegerField()),
                ('id_section', models.IntegerField()),
                ('id_cargo', models.IntegerField(default=0)),
                ('id_vinculo', models.IntegerField(default=0)),
                ('id_municipio', models.IntegerField()),
                ('id_funcao', models.IntegerField(default=0)),
                ('nome', models.CharField(max_length=100)),
                ('ativo', models.IntegerField(default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Setor',
        ),
        migrations.AddConstraint(
            model_name='departamento',
            constraint=models.UniqueConstraint(fields=('departamento', 'id_municipio'), name='unique departamento departamento'),
        ),
        migrations.AlterModelTable(
            name='departamento',
            table='Departamento',
        ),
    ]
