# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,Funcionario,Folha
from django.db import connection


def searchDepartamento(id_municipio,chave,tipo):
    if tipo=='nome':
        obj=Departamento.objects.filter(id_municipio=id_municipio).filter(departamento=chave).first()
    else:
        obj=Departamento.objects.filter(id_municipio=id_municipio).filter(codigo=chave).first()

    if obj is None:
        id_departamento=0
    else:
        id_departamento=obj.id_departamento
    return id_departamento

def searchSetor(id_municipio,chave,tipo):
    if tipo=='nome':
        obj=Setor.objects.filter(id_municipio=id_municipio).filter(setor=chave).first()
    else:
        obj=Setor.objects.filter(id_municipio=id_municipio).filter(codigo=chave).first()
    if obj is None:
        id_setor=0
    else:
        id_setor=obj.id_setor
    return id_setor




def searchCargo(id_municipio,nome_do_cargo):
    obj=Cargo.objects.filter(id_municipio=id_municipio).filter(cargo=nome_do_cargo).first()
    if obj is None:
        Cargo.objects.create(id_municipio=id_municipio,cargo=nome_do_cargo)
        obj=Cargo.objects.filter(id_municipio=id_municipio,cargo=nome_do_cargo).first()
        id_cargo=obj.id_cargo
    else:
        id_cargo=obj.id_cargo
    return id_cargo



def searchVinculo(id_municipio,nome_do_vinculo):
    obj=Vinculo.objects.filter(id_municipio=id_municipio).filter(vinculo=nome_do_vinculo).first()
    if obj is None:
        Vinculo.objects.create(id_municipio=id_municipio,vinculo=nome_do_vinculo)
        obj=Vinculo.objects.filter(id_municipio=id_municipio,vinculo=nome_do_vinculo).first()
        id_vinculo=obj.id_vinculo
    else:
        id_vinculo=obj.id_vinculo
    return id_vinculo

def searchProvDesc(id_municipio,tipo,codigo,descricao,incluir):
    obj=ProvDesc.objects.filter(id_municipio=id_municipio).filter(codigo=codigo).first()
    if obj is None:
        if incluir:
            ProvDesc.objects.create(id_municipio=id_municipio,tipo=tipo,codigo=codigo,descricao=descricao)
            obj=ProvDesc.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
            id_provdesc=obj.id_provdesc
        else:
            id_provdesc=0
    else:
        id_provdesc=obj.id_provdesc
    return id_provdesc


def mesPorExtenso(mes):
    if int(mes)==1:
        return 'JANEIRO'
    elif int(mes)==2:
        return 'FEVEREIRO'
    elif int(mes)==11:
        return 'NOVEMBRO'



def gravarFuncionario_local(codigo,nome,id_dep,id_set,id_cargo,id_vinculo):
    

    cursor = connection.cursor()

    cursor.execute("INSERT INTO tab_funcionario (codigo,nome,id_dep,id_setor,id_cargo,id_vinculo) values (%s,%s,%s,%s,%s,%s)", [codigo,nome,id_dep,id_set,id_cargo,id_vinculo])

    cursor.close()
    del cursor
    connection.close()



def gravarFuncionario(id_municipio,codigo,nome,id_dep,id_set,id_cargo,id_vinculo):
    obj = Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
    if obj is None:
        Funcionario.objects.create(
            id_departamento = id_dep,
            id_setor = id_set,
            id_cargo = id_cargo,
            id_vinculo = id_vinculo,
            id_municipio = id_municipio,
            nome = nome,
            codigo = codigo
            )

def proventosFuncionario(id_municipio,anomes,id_funcionario):
    lista=[]
    objs = ProvDesc.objects.filter(id_municipio=id_municipio,tipo='V').order_by('ordenacao1')
    for obj in objs:
        id_obj=obj.id_provdesc
        obj_f=Folha.objects.filter(id_municipio=id_municipio,anomes=anomes,id_funcionario=id_funcionario,id_provento=id_obj).first()
        if obj_f is not None:
            valor=obj_f.valor
        else:
            valor=0
        lista.append(str(valor))
    return lista


def cabecalhoFolha(id_municipio):
    lista=['Departamento','Setor','Codigo','Nome','Cargo','Vinculo']
    objs=ProvDesc.objects.filter(id_municipio=id_municipio,tipo='V').order_by('ordenacao1')
    for obj in objs:
        lista.append(obj.descricao)
    return lista





