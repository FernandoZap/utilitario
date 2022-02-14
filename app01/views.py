from django.shortcuts import render
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import incluirTramitacao,leituraZip,funcoes_gerais
from django.urls import reverse
#from .forms import f001_Tramitacoes,Folha_01Form
from django.contrib.auth.decorators import login_required
from .models import Municipio,Departamento,Setor
from accounts.models import User
import csv
import datetime
import os
import json
import mysql.connector
import openpyxl
import re
from django.core.files import File
import zipfile
from django.db import connection
#from zipfile import ZipFile

#https://docs.djangoproject.com/en/4.0/topics/db/sql/


def sessao(request):
    if not request.session.get('username'):
        request.session['username'] = request.user.username
    return



def processUserInfo(request,userInfo):
    #userInfo = json.loads(userInfo)
    print()
    print("USER INFO RECEIVED")
    print('--------------------------')
    #print(f"User Name: {userInfo['name']}")
    #print(f"User Type: {userInfo['type']}")
    print()
    return "Info received successfuly"


@login_required
def lendozip_modelo1(request):
    #Departamento.xtruncate()
    #Setor.truncate()
    #Vinculo.truncate()
    if (request.method == "POST" and request.FILES['filename']):
        #current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        tabela=request.POST['tabela']
        ano=request.POST['ano']
        mes=request.POST['mes']
        mes_extenso = funcoes_gerais.mesPorExtenso(mes)
        referencia='FOLHA REF:'+mes_extenso+'/'+ano
        anomes=ano+mes


        municipio = Municipio.objects.get(id_municipio=id_municipio)
        modelo = municipio.modelo
        string_pesquisa = municipio.string_pesquisa

        if leituraZip.valida_zip2(file_zip,string_pesquisa,referencia)==1:
            print ('processando arquivo zip')
        else:
            print ('arquivo nao corresponde')

        if leituraZip.valida_zip2(file_zip,string_pesquisa,referencia)==1:
            if modelo==1:
                if tabela=='departamento':
                    print ('processando departamento')
                    leituraZip.gravarDepartamento_modelo1(file_zip,id_municipio)
                else:
                    if tabela=='setor':
                        print ('processando setor')
                        leituraZip.gravarSetor_modelo1(file_zip,id_municipio)
                    else:
                        if tabela=='cargo':
                            print ('processando cargo')
                            leituraZip.gravarCargo_modelo1(file_zip,id_municipio)
                        else:
                            if tabela=='folha':
                                print ('processando folha')
                                leituraZip.gravarFolha_modelo1(file_zip,id_municipio,anomes)
                            else:
                                if tabela=='funcionario':
                                    print ('processando funcionario')
                                    leituraZip.funcionario_modelo1(file_zip,id_municipio,anomes)
                                else:
                                    if tabela=='folha_csv':
                                        leituraZip.folhacsv_modelo1(request,id_municipio,anomes)



            else:
                if modelo==2:
                    if tabela=='departamento':
                        leituraZip.departamento_modelo2(file_zip,id_municipio)
                    else:
                        if tabela=='setor':
                            leituraZip.setor_modelo2(file_zip,id_municipio)

        return HttpResponseRedirect(reverse('app01:lendozip'))
        #return render(request, 'app01/teste.html')
    else:
        titulo = 'Inclusao de Deptos/Setores/Funcionarios'
        municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/lendozip.html',
            {
                'titulo': titulo,
                'municipios':municipios
            }
          )


def lendozipFuncionario(request):
    #Departamento.truncate()
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])

        depto=""
        setor=""
        funcionario=""
        lista_depto=[]
        lista_setor=[]
        lista_funcionario=[]        


        zip = zipfile.ZipFile(file_zip)

        kk=0
        for filename in zip.namelist():

            #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
            arquivo =  filename
            folha=''
            funcionario=''
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')

                res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
                if res:
                    lista_depto.append(line[0:50])
                    depto=line[0:3]
                else:
                    if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                        cp=len(line)-4
                        lista_setor.append(line[0:3]+depto+line[-cp:])

                kk+=1
                #if kk>10500:
                    #break
            set_depto=[] #set(lista_depto)
            set_setor=set(lista_setor)
            for dep in set_depto:
                id_depto=int(dep[0:3])
                codigo=dep[5:10]
                departamento=dep[-(len(dep)-12):]
                search_dep=Departamento.objects.filter(id_depto=id_depto,id_municipio=id_municipio).first()
                if search_dep==None:
                    Departamento.objects.create(id_depto=id_depto,id_municipio=id_municipio,codigo=codigo,departamento=departamento)

            for st in set_setor:
                id_setor=int(st[0:3])
                id_depto=int(st[3:6])
                cp=len(st)-6
                setor=st[-cp:]
                setor=setor[0:50]
                #print ('setor: '+id_setor+';'+id_depto+';'+setor)


                search_dep=Setor.objects.filter(id_setor=id_setor,id_depto=id_depto,id_municipio=id_municipio).first()
                if search_dep==None:
                    Setor.objects.create(id_setor=id_setor,id_depto=id_depto,id_municipio=id_municipio,setor=setor)



                #print ('departamento: '+dep[0:3]+';'+dep[5:10]+';'+dep[-(len(dep)-12):])

        return HttpResponseRedirect(reverse('app01:folha_01'))
    else:
        titulo = 'Cadastro de Folha Leitura Arquivo Zip'
        municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/lendozipFuncionario.html',
            {
                'titulo_pagina': titulo,
                'municipios':municipios
            }
          )

def departamentoList(request):
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        print ('id_municipio: '+str(id_municipio))


        deptos = Departamento.objects.filter(id_municipio=id_municipio).order_by('departamento')
    else:
        deptos = []

    titulo = 'Lists dos Departamentos'
    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/deptoList.html',
            {
                'titulo': titulo,
                'departamentos':deptos,
                'municipios':municipios
            }
          )


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def setorList1(request):
    cursor = connection.cursor()

    #sql = 'Select distinct f.codigo_funcionario,d.codigo,d.departamento,s.codigo,s.setor,c.cargo,f.tipo,f.valor from folha f, departamento d,setor s, cargo c  where f.id_departamento=d.id_departamento and f.id_setor=s.id_setor and f.id_cargo=c.id_cargo order by f.codigo_funcionario,f.tipo'
    #sql = 'select * from view_dep_setor'
    #sql = 'Call my_proc_IN2(76)'
    sql2 = "SELECT f001_total_folha (76,202111,'R')"


    #cursor.execute(sql)
    #r = cursor.fetchall()
    #r = dictfetchall(cursor)

    cursor.execute(sql2)
    r2 = cursor.fetchall()
    #r2 = dictfetchall(cursor)

    r5 =  (r2[0])[0]

    cursor.close()
    del cursor
    #db_connection.close()

    #print (str(r[0][0])+';'+str(r[0][1])+';'+str(r[0][2])+';'+str(r[0][3]))
    
    return render (request, 'app01/output.html',{'valor':r5})



def setorList(request):
    #obj = Folha.objects.all()
    
    return render (request, 'app01/output.html',{'data':obj})




def listDepSetor(request):

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio


    else:
        municipio=''
    municipios = Municipio.objects.all()
    titulo = 'Lists dos Departamentos'

    sql = "select * from f006_listDepSetor('"+municipio+"')"
    cursor = connection.cursor()

    cursor.execute(sql)
    #r = cursor.fetchall()
    r = dictfetchall(cursor)


    return render(request, 'app01/listDepSetor.html',
            {
                'titulo': titulo,
                'departamentos':r,
                'municipios':municipios
            }
          )




def listFolhaResumo(request):

    opcao=''
    query1=None
    query2=None

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        opcao=request.POST['opcao']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

    else:
        id_municipio=0
        anomes=200001
        municipio=''
        referencia=''
    titulo = 'Totais da Folha'

    if opcao=='01':
        sql = "SELECT * FROM v002_listfolharesumo WHERE id_municipio="+str(id_municipio)+" AND "+" anomes="+str(anomes)+" order by departamento,setor"
            
            


    if opcao!='':
        cursor = connection.cursor()
        if opcao=='01':
            cursor.execute(sql)    
        else:
            params=(76,202111)
            cursor.execute("SELECT v.id_departamento,d.departamento,p.codigo,p.descricao,SUM(vantagem) as vantagem, SUM(desconto) AS desconto FROM v003_proventos v,provdesc p,departamento d WHERE v.id_departamento=d.id_departamento AND  v.id_provento=p.id_provdesc AND v.id_municipio=%s AND v.anomes=%s  GROUP BY v.id_departamento,d.departamento,p.codigo,p.descricao ORDER BY d.departamento", [id_municipio,anomes])    
        if opcao=='01':
            query1 = dictfetchall(cursor)
        else:
            query2 = dictfetchall(cursor)

    municipios = Municipio.objects.all()


    return render(request, 'app01/listFolhaResumo1.html',
            {
                'titulo': titulo,
                'resumo_depsetor':query1,
                'resumo_provento':query2,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia
            }
          )




def gravarCSVFolha(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)

    
        response = HttpResponse(content_type='text/csv')



        response['Content-Disposition'] = 'attachment; filename="folha_20210214.csv"'
        if (1==1):
            sql_command =   """
            select * from v006_folha where id_municipio=%s and anomes=%s order by id_funcionario;
                """

        try:
            db_cursor = connection.cursor()
            db_cursor.execute(sql_command, (id_municipio,anomes,))

            row = db_cursor.fetchone() 

            cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
            #print (cabecalho)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)

            contador=0
            while row and contador<17000:
                contador=contador+1
                id_funcionario=row[2]
                itens=[]
                lista=[]

                lista = funcoes_gerais.proventosFuncionario(id_municipio,anomes,id_funcionario)
                #print (lista)

                itens = [row[3],row[4],row[5],row[6],row[7],row[8]]
                for kk in range(0, len(lista)):
                   itens.append(lista[kk])
                   print (str(kk)+'. '+lista[kk])

                writer.writerow(itens)
                row = db_cursor.fetchone() 
            db_cursor.close()
            del db_cursor
            connection.close()
            
        finally:
            print ("Erro na inclusao")
            
        return response
    else:
        titulo = 'Dados Gerais do Pasta'
        municipios=Municipio.objects.all()
    return render(request, 'app01/gravarCSVFolha.html',
        {
            'titulo_pagina': titulo,
            'municipios':municipios

        }
    )
