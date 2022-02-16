from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import incluirTramitacao,leituraZip,funcoes_gerais
from django.urls import reverse
#from .forms import f001_Tramitacoes,Folha_01Form
from django.contrib.auth.decorators import login_required
from .models import Municipio,Departamento,Setor,ProvDesc,Folha
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

@login_required
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


@login_required
def setorList(request):
    #obj = Folha.objects.all()
    
    return render (request, 'app01/output.html',{'data':obj})


@login_required
def listDepSetor(request):

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio


    else:
        municipio=''
    municipios = Municipio.objects.all().order_by('municipio')
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

@login_required
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
            cursor.execute("SELECT p.codigo,p.descricao,SUM(vantagem) as vantagem, SUM(desconto) AS desconto FROM v003_proventos v,provdesc p,departamento d WHERE v.id_departamento=d.id_departamento AND  v.id_provento=p.id_provdesc AND v.id_municipio=%s AND v.anomes=%s  GROUP BY p.codigo,p.descricao", [id_municipio,anomes])    
        if opcao=='01':
            query1 = dictfetchall(cursor)
        else:
            query2 = dictfetchall(cursor)

    municipios = Municipio.objects.all().order_by('municipio')


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


@login_required
def gravarCSVFolha(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)

        obj = Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).first()
        if obj is None:
            municipios=Municipio.objects.all().order_by('municipio')
            return render(request, 'app01/gravarCSVFolha.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipios':municipios,
                        'mensagem':'O arquivo Zip ainda não foi importado'

                    }
                )




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
                id_funcionario=row[10]
                itens=[]
                lista=[]

                lista = funcoes_gerais.proventosFuncionario(id_municipio,anomes,id_funcionario)
                #print (lista)

                itens = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                for kk in range(0, len(lista)):
                   itens.append(lista[kk])
                   #print (str(kk)+'. '+lista[kk])

                writer.writerow(itens)
                row = db_cursor.fetchone() 
            db_cursor.close()
            del db_cursor
            connection.close()
            
        finally:
            print ("Erro na inclusao")
            
        return response

    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.all()
    return render(request, 'app01/gravarCSVFolha.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )


@login_required
def importacaoGeral(request):
    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Inclusao de Deptos/Setores/Funcionarios'
    municipios=Municipio.objects.all().order_by('municipio')

    if (request.method == "POST" and request.FILES['filename']):

        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)

        Folha.truncate()


        '''
        obj = Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).first()
        if obj is not None:
            
            mensagem='Essa Folha já foi importada!'
            return render(request, 'app01/importacaoGeral.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
        '''

        municipio = Municipio.objects.get(id_municipio=id_municipio)
        modelo = municipio.modelo
        string_pesquisa = municipio.string_pesquisa


        mes_extenso = funcoes_gerais.mesPorExtenso(mes,modelo)
        if id_municipio==76:
            referencia='FOLHA REF:'+mes_extenso+'/'+ano
        elif id_municipio==86:
            referencia='REF.:'+mes_extenso+' de '+ano


        if leituraZip.valida_zip(file_zip,string_pesquisa,referencia)==1:
            if modelo==1:
                leituraZip.importacaoGeral_modelo1(file_zip,id_municipio,anomes)
                leituraZip.importacaoProventos_modelo1(file_zip,id_municipio,anomes)
                leituraZip.importacaoFuncionario_modelo1(file_zip,id_municipio,anomes)
            if modelo==2:
                leituraZip.importacaoGeral_modelo2(file_zip,id_municipio,anomes)
                leituraZip.importacaoProventos_modelo2(file_zip,id_municipio,anomes)
                leituraZip.importacaoFuncionario_modelo2(file_zip,id_municipio,anomes)
        else:
            mensagem='Arquivo Zip não foi localizado!'
            return render(request, 'app01/importacaoGeral.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
                  )



        return HttpResponseRedirect(reverse('app01:importacaoGeral'))
    return render(request, 'app01/importacaoGeral.html',
            {
                'titulo': titulo_html,
                'municipios':municipios,
                'mensagem':''
            }
          )

@login_required
def gerandoFolha_modelo1(request):
    titulo_html='Importação da Folha de Pagamento'
    municipios = Municipio.objects.all().order_by('municipio')
    mensagem=''
    if (request.method == "POST" and request.FILES['filename']):
        #current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        mes_extenso = funcoes_gerais.mesPorExtenso(mes)
        referencia='FOLHA REF:'+mes_extenso+'/'+ano
        anomes=int(ano+mes)

        Folha.truncate()

        '''

        obj = Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).first()
        if obj is not None:
            
            mensagem='Essa Folha já foi importada!'
            return render(request, 'app01/lendozip.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
                  )
        '''

        municipio = Municipio.objects.get(id_municipio=id_municipio)
        modelo = municipio.modelo
        string_pesquisa = municipio.string_pesquisa

        if leituraZip.valida_zip(file_zip,string_pesquisa,referencia)==1:
            if modelo==1:
                leituraZip.gravarFolha_modelo1(file_zip,id_municipio,anomes)
        else:
            mensagem='O arquivo Zip não foi localizado!'
            return render(request, 'app01/lendozip.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
                  )

        return HttpResponseRedirect(reverse('app01:lendozip'))
    return render(request, 'app01/lendozip.html',
            {
                'titulo': titulo_html,
                'municipios':municipios,
                'mensagem':mensagem
            }
          )

