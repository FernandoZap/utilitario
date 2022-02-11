# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,Folha


def searchDepartamento(id_municipio,departamento):
    obj=Departamento.objects.filter(id_municipio=id_municipio).filter(departamento=departamento).first()
    if obj is None:
        id_departamento=0
    else:
        id_departamento=obj.id_departamento
    return id_departamento

def searchSetor(id_municipio,setor):
    obj=Setor.objects.filter(id_municipio=id_municipio).filter(setor=setor).first()
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




