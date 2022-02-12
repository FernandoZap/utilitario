from django import template
from app01.models import Folha
from django.db import connection

register = template.Library()



@register.simple_tag
def total_folha():

    return Folha.objects.count()


@register.simple_tag
def total_folha_mes(id_municipio,anomes,tipo):

    cursor = connection.cursor()

    sql = "select f007_somaFolha("+str(id_municipio)+","+str(anomes)+",'"+tipo+"')"

    cursor.execute(sql)
    #r0 = cursor.fetchall()
    r0 = dictfetchall(cursor)

    r1 =  (r0[0])[0]

    cursor.close()
    del cursor


    return r1



@register.simple_tag
def total_departamento(id_municipio,anomes,tipo,id_departamento):

    cursor = connection.cursor()

    sql = "SELECT f002_total_departamento("+str(id_municipio)+","+str(anomes)+",'"+tipo+"',"+str(id_departamento)+")"

    cursor.execute(sql)
    r0 = cursor.fetchall()
    #r2 = dictfetchall(cursor)

    r1 =  (r0[0])[0]

    cursor.close()
    del cursor


    return r1


@register.simple_tag
def total_setor(id_municipio,anomes,tipo,id_departamento,id_setor):

    cursor = connection.cursor()

    sql = "SELECT f003_total_setor("+str(id_municipio)+","+str(anomes)+",'"+tipo+"',"+str(id_departamento)+","+str(id_setor)+")"

    cursor.execute(sql)
    r0 = cursor.fetchall()
    #r2 = dictfetchall(cursor)

    r1 =  (r0[0])[0]

    cursor.close()
    del cursor


    return r1

