# Generated by Django 4.0.1 on 2022-02-06 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0034_delete_vinculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vinculo',
            fields=[
                ('id_vinculo', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('vinculo', models.CharField(max_length=100)),
                ('ativo', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'vinculo',
            },
        ),
        migrations.AddConstraint(
            model_name='vinculo',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'vinculo'), name='unique vinculo'),
        ),
    ]
