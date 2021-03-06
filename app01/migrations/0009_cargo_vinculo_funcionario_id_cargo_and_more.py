# Generated by Django 4.0.1 on 2022-02-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_funcionario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_municipio', models.IntegerField()),
                ('cargo', models.CharField(max_length=100)),
                ('ativo', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Vinculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_municipio', models.IntegerField()),
                ('vinculo', models.CharField(max_length=100)),
                ('ativo', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='funcionario',
            name='id_cargo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='id_vinculo',
            field=models.IntegerField(default=0),
        ),
    ]
