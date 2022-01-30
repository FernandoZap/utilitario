
from django.db import models

class Foha_01(models.Model):
    anomes = models.IntegerField()
    id_setor = models.IntegerField()
    id_funcionario = models.IntegerField()
    id_provento = models.IntegerField()
    valor = models.DecimalField(max_digits=9, decimal_places=2)



