from django.shortcuts import render
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import incluirTramitacao,leituraZip
from django.urls import reverse
#from .forms import f001_Tramitacoes,Folha_01Form
from django.contrib.auth.decorators import login_required
from .models import Municipio,Departamento
from accounts.models import User
#from accounts.conexoes import connections
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


@login_required
def v001_folha_01(request):
    pass

    #inclusaoDeUsuarios.inclusao()
    '''
    sessao(request)
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        operacao=request.POST['operacao']
        tramitacao=request.POST['tramitacao']
        planilha=request.FILES['filename']
        print ("operacao "+operacao)

        wb = openpyxl.load_workbook(planilha)
        sheets = wb.sheetnames
        sheet = wb.get_sheet_by_name(sheets[0])
        
        
        row = 2

        finalizar=0


        while row<sheet.max_row+1 and row<6:
            id_setor = str(sheet['A' + str(row)].value)
            id_funcionario = str(sheet['B' + str(row)].value)
            id_provento = str(sheet['C' + str(row)].value)
            valor = str(sheet['D' + str(row)].value)
            anomes=202112
            row+=1
            p = Foha_01(anomes=anomes,id_setor=id_setor, id_funcionario=id_funcionario, \
                id_provento=id_provento, valor=valor)
            p.save()



        return HttpResponseRedirect(reverse('app01:folha_01'))
    else:
        
        titulo = 'Cadastro de Folha_01'
        form = Folha_01Form()
    return render(request, 'app01/folha_01.html',
            {
                'form':form,
                'titulo_pagina': titulo,
                'usuario':request.session['username']
            }
          )

    '''


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
def v001_folha_02(request):
    #inclusaoDeUsuarios.inclusao()
    sessao(request)
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        operacao=request.POST['operacao']
        tramitacao=request.POST['tramitacao']
        file=request.FILES['filename']

        file1 = open(file, 'r')
        for linha in file1:
            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', linha)
            if res:
                print ('setor' + ' - ' + linha[0:50])
        file1.close()



        return HttpResponseRedirect(reverse('app01:folha_02'))
    else:
        
        titulo = 'Cadastro de Folha_01'
        form = Folha_01Form()
    return render(request, 'app01/folha_02.html',
            {
                'form':form,
                'titulo_pagina': titulo,
                'usuario':request.session['username']
            }
          )

def lendozip(request):
    #Departamento.xtruncate()
    #Setor.truncate()
    #Vinculo.truncate()
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        tabela=request.POST['tabela']
        ano=request.POST['ano']
        mes=request.POST['mes']
        referencia='FOLHA REF:'+mes+'/'+ano
        anomes='202111'

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
                    leituraZip.departamento_modelo1(file_zip,id_municipio)
                else:
                    if tabela=='setor':
                        leituraZip.setor_modelo1(file_zip,id_municipio)
                    else:
                        if tabela=='folha':
                            leituraZip.gravarFolha_modelo1(file_zip,id_municipio,anomes)
                        else:
                            if tabela=='funcionario':
                                leituraZip.funcionario_modelo1(file_zip,id_municipio,anomes)


            else:
                if modelo==2:
                    if tabela=='departamento':
                        leituraZip.departamento_modelo2(file_zip,id_municipio)
                    else:
                        if tabela=='setor':
                            leituraZip.setor_modelo2(file_zip,id_municipio)


        return HttpResponseRedirect(reverse('app01:lendozip'))
    else:
        titulo = 'Inclusao de Deptos/Setores/Funcionarios'
        municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/lendozip.html',
            {
                'titulo': titulo,
                'municipios':municipios
            }
          )

def lendozipFolha(request):
    #Departamento.xtruncate()
    #Setor.truncate()
    #Vinculo.truncate()
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        anomes=request.POST['anomes']

        municipio = Municipio.objects.get(id_municipio=id_municipio)
        modelo = municipio.modelo
        string_pesquisa = municipio.string_pesquisa

        if leituraZip.valida_zip(file_zip,string_pesquisa)==1:
            print ('processando arquivo zip')
        else:
            print ('arquivo nao corresponde')

        if leituraZip.valida_zip(file_zip,string_pesquisa)==1:
            if modelo==1:
                if tabela=='departamento':
                    leituraZip.departamento_modelo1(file_zip,id_municipio)
                else:
                    if tabela=='setor':
                        leituraZip.setor_modelo1(file_zip,id_municipio)
                    else:
                        if tabela=='funcionario':
                            leituraZip.funcionario_modelo1(file_zip,id_municipio)

            else:
                if modelo==2:
                    if tabela=='departamento':
                        leituraZip.departamento_modelo2(file_zip,id_municipio)
                    else:
                        if tabela=='setor':
                            leituraZip.setor_modelo2(file_zip,id_municipio)


        return HttpResponseRedirect(reverse('app01:lendozip'))
    else:
        titulo = 'Inclusao de Deptos/Setores/Funcionarios'
        municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/lendozip.html',
            {
                'titulo': titulo,
                'municipios':municipios
            }
          )



def lendozipDepto(request):
    pass
    #Departamento.truncate()
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])

        depto=""
        lista_depto=[]


        zip = zipfile.ZipFile(file_zip)

        kk=0
        for filename in zip.namelist():

            #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
            arquivo =  filename
            folha=''
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')

                res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
                if res:
                    lista_depto.append(line[0:50])
                    depto=line[0:3]

                kk+=1
                #if kk>10500:
                    #break
            set_depto=set(lista_depto)
            for dep in set_depto:
                id_depto=int(dep[0:3])
                codigo=dep[5:10]
                departamento=dep[-(len(dep)-12):]
                search_dep=Departamento.objects.filter(id_depto=id_depto,id_municipio=id_municipio).first()
                if search_dep==None:
                    Departamento.objects.create(id_depto=id_depto,id_municipio=id_municipio,codigo=codigo,departamento=departamento)



        return HttpResponseRedirect(reverse('app01:folha_01'))
    else:
        titulo = 'Cadastro de Folha Leitura Arquivo Zip (Departamento)'
        municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/lendozipDepto.html',
            {
                'titulo_pagina': titulo,
                'municipios':municipios
            }
          )

def lendozipSetor(request):
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
    return render(request, 'app01/lendozipSetor.html',
            {
                'titulo_pagina': titulo,
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

'''
incluirTramitacao.choicesMunicipios()
deptos = Departamento.objects.all().order_by('departamento')
titulo = 'Departamentos'
return render(request, 'app01/deptoList.html',{'departamentos':deptos,'titulo':titulo})
'''

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]



def setorList(request):
    cursor = connection.cursor()

    #sql = 'Select distinct f.codigo_funcionario,d.codigo,d.departamento,s.codigo,s.setor,c.cargo,f.tipo,f.valor from folha f, departamento d,setor s, cargo c  where f.id_departamento=d.id_departamento and f.id_setor=s.id_setor and f.id_cargo=c.id_cargo order by f.codigo_funcionario,f.tipo'
    #sql = 'select * from view_dep_setor'
    sql = 'Call my_proc_IN(76)'

    cursor.execute(sql)
    #r = cursor.fetchall()
    r = dictfetchall(cursor)

    #print (str(r[0][0])+';'+str(r[0][1])+';'+str(r[0][2])+';'+str(r[0][3]))
    
    return render (request, 'app01/output.html',{'data':r})