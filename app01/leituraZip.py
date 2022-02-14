# -*- coding: utf-8 -*-
import os
import sys
import datetime
import zipfile
import re
from .models import Departamento,Setor,Cargo,Vinculo,ProvDesc,Folha,Funcionario
import csv
from . import funcoes_gerais
from django.db import connection
from django.http import HttpResponse


#gravarDepartamento_modelo1
#gravarSetor_modelo1
#gravarCargo_modelo1

    
def valida_zip1(file_zip,string_pesquisa,referencia):


    pesquisa=re.compile(string_pesquisa)

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                res = pesquisa.search(line)
                if res is None:
                    zip.close()
                    print ('fechando o valida_zip1 SEM sucesso  e com retorno 0')
                    return 0
                else:
                    zip.close()
                    print ('fechando o valida_zip1 COM sucesso e retorno 1')
                    return 1

def valida_zip2(file_zip,string_pesquisa,referencia):

    pesquisa_municipio=re.compile(string_pesquisa)
    pesquisa_anomes=re.compile(referencia)
    pesquisa1=0
    pesquisa2=0

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                res1 = pesquisa_municipio.search(line)
                res2 = pesquisa_anomes.search(line)
                if res1 is not None:
                    pesquisa1=1
                if res2 is not None:
                    pesquisa2=1
                contador+=1
                if contador>7:
                    if pesquisa1==0 or pesquisa2==0:
                        zip.close()
                        print ('fechando SEM sucesso!')
                        return 0
                    else:
                        zip.close()
                        print ('fechando COM sucesso!')
                        return 1


def departamento_modelo2(file):
    pass


def folha_modelo1(file_zip,id_municipio,anomes):

        depto=""
        setor=""
        lista_setor=[]


        zip = zipfile.ZipFile(file_zip)

        for filename in zip.namelist():

            #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')

                res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
                if res:
                    depto=line[0:3]
                    nome_depto=line[12:61]
                else:
                    if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                        cp=len(line)-4
                        nome_setor=(line[4:43]).rstrip()
                        lista_setor.append(line[0:3]+';'+depto+';'+nome_setor+';'+nome_depto)
            set_setor=set(lista_setor)

            for st in set_setor:
                dados= st.split(';')
                cod_setor=dados[0]
                cod_depto=dados[1]
                nome_setor=(dados[2]).rstrip()
                nome_depto=(dados[3]).rstrip()
                #print (cod_setor+';'+cod_depto+';'+nome_setor+';'+nome_depto)
                if (nome_setor[0:29]=='SECRETARIA DESENVOLVIMENTO EC'):
                    nome_setor='SETOR NAO CADASTRADO'
                    print ('departamento: '+ nome_depto+';'+nome_setor+';'+str(id_municipio))
                    departamento=Departamento.objects.filter(id_municipio=id_municipio,departamento__contains=nome_depto).first()
                    if departamento is not None:
                        print ('pesquisando setor')
                        id_setor = funcoes_gerais.searchSetor(id_municipio,nome_setor,cod_setor,departamento.id_departamento)



def funcionario_modelo1(file_zip,id_municipio,anomes):
    # gravar os funcionarios
    depto=""
    setor=""
    lista_funcionario=[]

 

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        depto=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]


        lin_cargo=0
        lin_vinculo=0
         

        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=funcoes_gerais.searchDepartamento(id_municipio,depto,'codigo')
                            id_set=funcoes_gerais.searchSetor(id_municipio,setor,'codigo')
                            id_cargo=funcoes_gerais.searchCargo(id_municipio,cargo)
                            id_vinculo=funcoes_gerais.searchCargo(id_municipio,vinculo)




                            #lista_proventos.append(montaProventos(file_zip,codigo,depto,setor,cargo,vinculo,line_no))
                            #lista_provdesc.append(montaProvDesc(file_zip,codigo,depto,setor,cargo,vinculo,line_no))
                            #print (codigo+';'+vinculo)

                            #lista_funcionario.append(codigo+';'+nome.rstrip()+';'+str(id_dep)+';'+str(id_set)+';'+cargo.rstrip()+';'+vinculo.rstrip())
                            lista_funcionario.append(codigo+';'+nome.rstrip()+';'+str(id_dep)+';'+str(id_set)+';'+str(id_cargo)+';'+str(id_vinculo))
                            funcoes_gerais.gravarFuncionario(id_municipio,codigo,nome,id_dep,id_set,id_cargo,id_vinculo)
                            #print (codigo)


            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
            if res:
                depto=line[0:11]
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=line[0:3]
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        depto==''
                        setor==''

        set_funcionario=set(lista_funcionario)
        for st in set_funcionario:
            dados=st.split(';')
            id_funcionario=int(dados[0])
            id_depto=int(dados[2])
            id_setor=int(dados[3])
            cargo=(dados[4]).rstrip()
            vinculo=(dados[5]).rstrip()
            #print ('0='+dados[0]+';'+'1='+dados[1]+';'+'2='+dados[2]+';'+'3='+dados[3]+';'+'4='+dados[4]+';'+'5='+dados[5])
    zip.close()
    '''
    # Listar os proventos e descontos
    set_provdesc=set()
    for subset1 in lista_provdesc:
        for subset2 in subset1:
            set_provdesc.add(subset2)
    for subset3 in set_provdesc:
        tipo5=subset3[0:1]
        codigo5=subset3[1:4]
        descricao5=subset3[-(len(subset3)-4):]

        retorno = searchProvDesc(id_municipio,tipo5,codigo5,descricao5)

    with open('folha_novembro.csv', mode='w', newline='') as csv_file:
    
        fieldnames = ["Func", "Departamento", "Setor", "Id_cargo", "Cargo", "Id_vinculo", "Vinculo","Tipo", "Cod", "Provento", "Valor"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for ls in lista_proventos:
            for rel in ls:
                codigo = rel['codigo']
                depto = rel['depto']
                setor = rel['setor']
                cargo = (rel['cargo']).rstrip()
                vinculo = (rel['vinculo']).rstrip()

                id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo)
                if id_cargo==0:
                    lista_cargo.append(cargo)
                id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo)
                if id_vinculo==0:
                    lista_vinculo.append(vinculo)

                provents = rel['proventos']
                
                for prov in provents:
                        #print(codigo+';'+prov['tipo']+';'+prov['codigo']+';'+prov['provento']+';'+prov['valor'])
                        writer.writerow({"Func":codigo, "Departamento":depto, "Setor":setor, "Id_cargo":id_cargo,"Cargo":cargo, "Id_vinculo": id_vinculo,"Vinculo":vinculo ,"Tipo": prov['tipo'], "Cod": prov['codigo'],'Provento':prov['provento'],'Valor':prov['valor']})

    '''




def montaProventos(file_zip,codigo,depto,setor,cargo,vinculo,line_num):
    line_num=line_num-2
    ok=0
    lista=[]
    lista_completa=[]

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                if line_no==line_num:
                    if codigo!=line[0:6]:
                        break
                    else:
                        ok=1
                if line_no>=line_num+2 and ok==1:
                    if re.search(r'[A-Z]+',line) and ok==1:
                        linha = (line.rstrip('\n')).rstrip('\r')
                        if (re.search(r'[0-9]{3}\s[A-Z]',linha)  or re.search(r'1/3 FERIAS',linha)) and ok==1:
                            prov_cod=(linha[40:43]).rstrip()
                            prov_desc=(linha[44:70]).rstrip()
                            prov_valor=(linha[70:79]).lstrip()
                            desc_cod=(linha[80:83]).rstrip()
                            desc_desc=(linha[84:110]).rstrip()
                            desc_valor=(linha[111:120]).lstrip()

                            if len(prov_cod)>0 and len(prov_valor)>0:
                                dados_prov={'tipo':'V','codigo':prov_cod,'provento':prov_desc,'valor':prov_valor}
                                lista.append(dados_prov)
                            if len(desc_cod)>0 and len(desc_valor)>0:
                                dados_desc={'tipo':'D','codigo':desc_cod,'provento':desc_desc,'valor':desc_valor}
                                lista.append(dados_desc)

                            #dados = codigo+';'+prov_cod+';'+prov_desc+';'+prov_valor+';'+desc_cod+';'+desc_desc+';'+desc_valor
                            #dados = codigo+';'+prov_cod+';'+prov_desc+';'+prov_valor+';'+desc_cod

                            #lista.append(dados)
                        else:
                            break

            lista_completa=[{'codigo':codigo,'depto':depto,'setor':setor,'cargo':cargo,'vinculo':vinculo,'proventos':lista}] 
        #filename.close()

    return lista_completa



def montaProvDesc(file_zip,codigo,depto,setor,cargo,vinculo,line_num):
    line_num=line_num-2
    ok=0
    lista=[]
    lista_completa=[]

    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        for filename in zip.namelist():
            file = zip.open(filename)
            for line_no, line in enumerate(file,1):
                line=line.decode('ISO-8859-1')
                if line_no==line_num:
                    if codigo!=line[0:6]:
                        break
                    else:
                        ok=1
                if line_no>=line_num+2 and ok==1:
                    if re.search(r'[A-Z]+',line) and ok==1:
                        linha = (line.rstrip('\n')).rstrip('\r')
                        if re.search(r'[0-9]{3}\s[A-Z]',linha) and ok==1:
                            prov_cod=(linha[40:43]).rstrip()
                            prov_desc=(linha[44:70]).rstrip()
                            prov_valor=(linha[70:79]).lstrip()
                            desc_cod=(linha[80:83]).rstrip()
                            desc_desc=(linha[84:110]).rstrip()
                            desc_valor=(linha[111:120]).lstrip()

                            if len(prov_cod)>0 and len(prov_valor)>0:
                                dados_prov='V'+prov_cod+prov_desc
                                lista.append(dados_prov)
                            if len(desc_cod)>0 and len(desc_valor)>0:
                                dados_desc='D'+desc_cod+desc_desc
                                lista.append(dados_desc)

                        else:
                            break

    return lista


def gravarFolha_modelo1(file_zip,id_municipio,anomes):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        departamento=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lin_cargo=0
        lin_vinculo=0
         

        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            if line_no>700:
                break
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=funcoes_gerais.searchDepartamento(id_municipio,departamento,'nome')
                            id_set=funcoes_gerais.searchSetor(id_municipio,setor,'nome')
                            if id_dep==0:
                                print ('depto: '+departamento)
                            if id_set==0:
                                print ('setor: '+setor)


                            lista_proventos.append(montaProventos(file_zip,codigo,id_dep,id_set,cargo,vinculo,line_no))

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                codigo=line[0:10]
                departamento=line[-(len(line)-12):]
                departamento=departamento[0:38]
                departamento=departamento.rstrip()

            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=(line[4:44]).rstrip()
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        departamento==''
                        setor==''

    zip.close()

    for ls in lista_proventos:
        for rel in ls:
            codigo = rel['codigo']
            depto = rel['depto']
            setor = rel['setor']
            cargo = rel['cargo']
            vinculo = rel['vinculo']
            id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo)
            if id_cargo==0:
                lista_cargo.append(cargo)
            id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo)
            if id_vinculo==0:
                lista_vinculo.append(vinculo)

            provents = rel['proventos']
            
            for prov in provents:
                    #print(codigo+';'+prov['tipo']+';'+prov['codigo']+';'+prov['provento']+';'+prov['valor'])
                    #writer.writerow({"Func":codigo, "Departamento":depto, "Setor":setor, "Id_cargo":id_cargo,"Cargo":cargo, "Id_vinculo": id_vinculo,"Vinculo":vinculo ,"Tipo": prov['tipo'], "Cod": prov['codigo'],'Provento':prov['provento'],'Valor':prov['valor']})
                    id_provdesc=funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],'',True)
                    #print (str(id_municipio)+';'+str(202111)+';'+codigo+';'+str(depto)+';'+\
                        #str(setor)+';'+str(id_cargo)+';'+str(id_vinculo)+str(id_provdesc)+';'+prov['tipo']+';'+str(prov['valor']))
                    valor = prov['valor']
                    valor = valor.replace('.','')
                    valor = valor.replace(',','.')
                    valor = float(valor)
                    if len(codigo)==6:
                        obj=Funcionario.objects.filter(id_municipio=id_municipio,codigo=codigo).first()
                        if obj is not None:
                            id_funcionario=obj.id_funcionario
                            Folha.objects.create(id_municipio=id_municipio,anomes=202111,id_funcionario=id_funcionario,\
                                id_departamento=depto,id_setor=setor,id_cargo=id_cargo,id_vinculo=id_vinculo,\
                                id_provento=id_provdesc,tipo=prov['tipo'],valor=valor)                    


def gravarDepartamento_modelo1(file_zip,id_municipio):

    zip = zipfile.ZipFile(file_zip)

    kk=0
    lista_depto=[]

    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                lista_depto.append(line[0:50])
                depto=line[0:3]

            kk+=1
            #if kk>10500:
                #break
        set_depto=set(lista_depto)
        for dep in set_depto:
            codigo=dep[0:10]
            departamento=dep[-(len(dep)-12):]
            departamento=departamento.rstrip()
            search_dep=Departamento.objects.filter(id_municipio=id_municipio,departamento=departamento).first()
            if search_dep==None:
                Departamento.objects.create(id_municipio=id_municipio,codigo=codigo,departamento=departamento)
    zip.close()


def gravarSetor_modelo1(file_zip,id_municipio):

    depto=""
    setor=""
    funcionario=""
    lista_depto=[]
    lista_setor=[]
    lista_funcionario=[]        


    zip = zipfile.ZipFile(file_zip)

    kk=0
    for filename in zip.namelist():

        arquivo =  filename
        folha=''
        funcionario=''
        departamento=''
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                if len(departamento)==0:
                    #lista_depto.append(line[0:50])
                    departamento=(line[12:50]).rstrip()
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    if len(departamento)>0:
                        cp=len(line)-4
                        lista_setor.append(line[0:3]+';'+departamento+';'+line[4:44])
                        departamento=''

            kk+=1
            #if kk>10500:
                #break
        set_setor=set(lista_setor)
        for st in set_setor:
            dados = st.split(';')
            cod_setor=dados[0]
            departamento=dados[1]
            setor=dados[2]
            setor=(setor).rstrip()

            obj_dep=Departamento.objects.filter(id_municipio=id_municipio,departamento=departamento).first()
            if obj_dep is None:
                id_depto=0
            else:
                id_depto=obj_dep.id_departamento


            search_dep=Setor.objects.filter(id_departamento=id_depto,id_municipio=id_municipio,setor=setor).first()
            if search_dep is None:
                Setor.objects.create(id_departamento=id_depto,id_municipio=id_municipio,setor=setor,codigo=cod_setor)
    zip.close()



def gravarCargo_modelo1(file_zip,id_municipio):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        depto=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargos=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lista1=[]
        lista2=[]


        lin_cargo=0
        lin_vinculo=0
         

        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            #id_dep=funcoes_gerais.searchDepartamento(id_municipio,depto)
                            #id_set=funcoes_gerais.searchSetor(id_municipio,setor)

                            #lista_proventos.append(montaProventos(file_zip,codigo,depto,setor,cargo,vinculo,line_no))
                            lista_cargos.append({'cargo':cargo,'vinculo':vinculo})


            res = re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line)
            if res:
                depto=line[0:3]
            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=line[0:3]
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        depto==''
                        setor==''

    zip.close()
    for ls in lista_cargos:
        cargo=ls['cargo']
        vinculo=ls['vinculo']
    
        cargo = cargo.rstrip()
        vinculo = vinculo.rstrip()

        id_cargo = funcoes_gerais.searchCargo(id_municipio,cargo)
        if id_cargo==0:
            lista1.append(cargo)
        id_vinculo = funcoes_gerais.searchVinculo(id_municipio,vinculo)
        if id_vinculo==0:
            lista2.append(vinculo)
    set_cargo=set(lista1)
    set_vinculo=set(lista2)
    for st in set_cargo:
        print ("cargo: "+st)
    for st in set_vinculo:
        print ("vinculo: "+st)




'''
def pesquisa(linha):
    lista=[]
    objs=ProvDesc.objects.all()
    for obj in objs:
        lista.append(obj.descricao)
    for l in lista:
        if re.search(r'[0-9]{3}\s[A-Z]',linha) and ok==1:
'''





def folhacsv_modelo1(request, id_municipio,anomes):


    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="processo.csv"'

    cursor = connection.cursor()

    cursor.execute("SELECT v.id_departamento,d.departamento,p.codigo,p.descricao,SUM(vantagem) as vantagem, SUM(desconto) AS desconto FROM v003_proventos v,provdesc p,departamento d WHERE v.id_departamento=d.id_departamento AND  v.id_provento=p.id_provdesc AND v.id_municipio=%s AND v.anomes=%s  GROUP BY v.id_departamento,d.departamento,p.codigo,p.descricao ORDER BY d.departamento", [id_municipio,anomes])                        

    row = cursor.fetchone() 

    print ("id_municipio "+str(id_municipio)+ '  anomes '+anomes)
    writer = csv.writer(response, delimiter=';')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow((
    'departamento',
    'descricao'
    ))

    contador=0
    while row and contador<25:
        contador=contador+1

        writer.writerow((
        row[1],
        row[3]
        ))
        row = cursor.fetchone() 
    cursor.close()
    del cursor
    connection.close()
                
    return response
                






def gravarPovDesc_modelo1(file_zip,id_municipio,anomes):
    depto=""
    setor=""
    lista_funcionario=[]

    zip = zipfile.ZipFile(file_zip)

    for filename in zip.namelist():
        departamento=""
        setor=""
        lista_funcionario=[]
        lista_proventos=[]
        lista_cargo=[]
        lista_vinculo=[]
        lista_provdesc=[]
        lin_cargo=0
        lin_vinculo=0
         

        #print (filename)  #imprime o nome dos arquivo txt que estão empacotados no arquivo zip
        file = zip.open(filename)
        for line_no, line in enumerate(file,1):
            #if line_no>700:
            #    break
            line=line.decode('ISO-8859-1')
            if line_no>4:
                if lin_cargo==line_no:
                    if re.search(r'\s{7}[A-Z]+',line):
                        cargo=(line[7:40]).rstrip()
                        lin_cargo=0
                        lin_vinculo=line_no+1
                else:
                    if lin_vinculo==line_no:
                        if re.search(r'\s{7}[A-Z]+',line):
                            vinculo=(line[7:40]).rstrip()
                            lin_vinculo=0
                            codigo=funcionario[0:6]
                            nome=funcionario[-53:]
                            id_dep=0 #funcoes_gerais.searchDepartamento(id_municipio,departamento,'nome')
                            id_set=0 #funcoes_gerais.searchSetor(id_municipio,setor,'nome')
                            #if id_dep==0:
                                #print ('depto: '+departamento)
                            #if id_set==0:
                                #print ('setor: '+setor)


                            lista_proventos.append(montaProventos(file_zip,codigo,id_dep,id_set,cargo,vinculo,line_no))

            if re.search(r'^[0-9]{3}[\s]\([0-9]{2}\.[0-9]{2}\)[\s][A-Z]{3,4}', line):
                codigo=line[0:10]
                departamento=line[-(len(line)-12):]
                departamento=departamento[0:38]
                departamento=departamento.rstrip()

            else:
                if re.search(r'^[0-9]{3}[\s][A-Z]{3}', line):
                    setor=(line[4:44]).rstrip()
                else:
                    if re.search(r'^[0-9]{6}[\s][A-Z]{3}', line):
                        #print(depto+';'+setor+';'+line[0:50])
                        funcionario=line[0:60]
                        lin_cargo=line_no+1
                        departamento==''
                        setor==''

    zip.close()

    for ls in lista_proventos:
        for rel in ls:
            codigo = rel['codigo']
            depto = rel['depto']
            setor = rel['setor']
            cargo = rel['cargo']
            vinculo = rel['vinculo']

            provents = rel['proventos']
            
            for prov in provents:
                #print(prov)
                funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],prov['provento'],True)
                    #print(codigo+';'+prov['tipo']+';'+prov['codigo']+';'+prov['provento']+';'+prov['valor'])
                    #writer.writerow({"Func":codigo, "Departamento":depto, "Setor":setor, "Id_cargo":id_cargo,"Cargo":cargo, "Id_vinculo": id_vinculo,"Vinculo":vinculo ,"Tipo": prov['tipo'], "Cod": prov['codigo'],'Provento':prov['provento'],'Valor':prov['valor']})
                    #id_provdesc=funcoes_gerais.searchProvDesc(id_municipio,prov['tipo'],prov['codigo'],'',True)

