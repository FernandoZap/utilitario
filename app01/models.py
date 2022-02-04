
from django.db import models

class Foha_01(models.Model):
    anomes = models.IntegerField()
    id_setor = models.IntegerField()
    id_funcionario = models.IntegerField()
    id_provento = models.IntegerField()
    valor = models.DecimalField(max_digits=9, decimal_places=2)


class Departamento(models.Model):  
    id_depto = models.IntegerField()
    id_municipio = models.IntegerField()
    codigo = models.CharField(max_length=50)  
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.departamento

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        




