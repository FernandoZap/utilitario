from __future__ import unicode_literals
from django.db import connection
from django.db import models


class Folha(models.Model):
    id_folha = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    anomes = models.IntegerField()
    id_funcionario = models.IntegerField()
    id_departamento = models.IntegerField()
    id_setor = models.IntegerField()
    id_cargo = models.IntegerField()
    id_vinculo = models.IntegerField()
    id_provento = models.IntegerField()
    tipo = models.CharField(max_length=1)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'folha'

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        


class Departamento(models.Model):  
    id_departamento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    codigo = models.CharField(max_length=50,default='')  
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.departamento

    class Meta:
            db_table = "departamento"  

    class Meta:
        db_table = 'departamento'
        constraints = [
            models.UniqueConstraint(fields=['departamento', 'id_municipio'], name='unique departamento departamento')
        ]



    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Municipio(models.Model):  
    id_municipio = models.AutoField(primary_key=True)
    municipio = models.CharField(max_length=100)
    modelo = models.IntegerField(default=0)
    string_pesquisa = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.municipio

    class Meta:
            db_table = "municipio"        

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        

class Setor(models.Model):  
    id_setor = models.AutoField(primary_key=True)
    id_departamento = models.IntegerField()
    id_municipio = models.IntegerField(default=0)
    setor = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.setor

    class Meta:
            db_table = "setor"        

    class Meta:
        db_table = 'setor'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'setor'], name='unique setor setor')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        


class Funcionario(models.Model):  
    id_funcionario = models.AutoField(primary_key=True)
    id_departamento = models.IntegerField()
    id_setor = models.IntegerField()
    id_cargo = models.IntegerField(default=0)
    id_vinculo = models.IntegerField(default=0)
    id_municipio = models.IntegerField()
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    data_admissao = models.DateField(null=True)
    ativo = models.IntegerField(default=1)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'funcionario'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'codigo'], name='funcionario unique codigo')
        ]


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Cargo(models.Model):  
    id_cargo = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    cargo = models.CharField(max_length=100)
    ativo = models.IntegerField(default=1)

    def __str__(self):
        return self.cargo

    class Meta:
        db_table = 'cargo'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'cargo'], name='unique cargo')
        ]


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        


class Vinculo(models.Model):  
    id_vinculo = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    vinculo = models.CharField(max_length=100)
    ativo = models.IntegerField(default=1)

    def __str__(self):
        return self.vinculo

    class Meta:
        db_table = 'vinculo'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'vinculo'], name='unique vinculo')
        ]


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        
    

class ProvDesc(models.Model):  
    id_provdesc = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    tipo = models.CharField(max_length=1) 
    codigo = models.CharField(max_length=6) 
    descricao = models.CharField(max_length=100)
    ordenacao1 = models.IntegerField(default=0)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'provdesc'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'codigo'], name='provdesc unique codigo')
        ]


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        
    
