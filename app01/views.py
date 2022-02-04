from django.shortcuts import render
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import incluirTramitacao
from django.urls import reverse
from .forms import f001_Tramitacoes,Folha_01Form
from django.contrib.auth.decorators import login_required
from .models import Foha_01
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
#from zipfile import ZipFile


@login_required
def v001_folha_01(request):
    #inclusaoDeUsuarios.inclusao()
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

def lendozip(request):
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser
        operacao=request.POST['operacao']
        tramitacao=request.POST['tramitacao']
        file_zip=request.FILES['filename']


        zip = zipfile.ZipFile(file_zip)

        kk=0
        for filename in zip.namelist():

            #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
            arquivo =  filename
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                if re.search(r'FOLHA',line):
                    print (line[0:10])
                else:
                    if re.search(r'021635',line):
                        #021635 JOSE VALDI COUTINHO
                        print (line[0:27])

                kk+=1
                if kk>20:
                    break
        return HttpResponseRedirect(reverse('app01:folha_01'))
    else:
        titulo = 'Cadastro de Folha_01'
        form = Folha_01Form()
    return render(request, 'app01/folha_01.html',
            {
                'form':form,
                'titulo_pagina': titulo,
            }
          )






