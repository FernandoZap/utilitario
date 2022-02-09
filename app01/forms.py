# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import Select, Widget
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import datetime
from . import choices,incluirTramitacao



class f001_Tramitacoes(forms.Form):
    OPERACAO_CHOICES=(
        ('BRANCO',''),
        ('EXCLUIR','Excluir tramitacao'),
        ('REAGENDAR','Reagendar tramitacao'),
        ('STATUS','Alterar Status'),
        ('INCLUIR','Incluir tramitacoes'),
    )

    operacao = forms.CharField(
        label = 'Operacao',
        widget=forms.Select(choices=OPERACAO_CHOICES),
        max_length=18
        )    
    tramitacao = forms.CharField(
        label = 'Tipo da tramitacao',
        widget=forms.Select(choices=choices.TRAMITACAO),
        max_length=50
        )
    documento = forms.FileField(label='Arquivo Excel')

    def clean_operacao(self):
        operation = self.cleaned_data.get('operacao')
        if(operation=='BRANCO'):
            raise forms.ValidationError("Informe ass operacao")
        return operation

    def execute(self,current_user):
        operacao = self.cleaned_data.get('operacao')
        tramitacao = self.cleaned_data.get('tramitacao')
        planilha = self.cleaned_data.get('documento')
        if(operacao=='INCLUIR'):
            incluirTramitacao.incluir(planilha,operacao,tramitacao,current_user)
        elif (operacao=='REAGENDAR' or operacao=='EXCLUIR'):
            #importarDecisoes3.exc_Tramitacao(planilha,operacao,tramitacao,current_user)
            incluirTramitacao.incluir(planilha,operacao,tramitacao,current_user)
        elif (operacao=='STATUS'):
            #importarDecisoes3.tramitacao_alterarStatus(planilha,operacao,tramitacao,current_user)
            incluirTramitacao.incluir(planilha,operacao,tramitacao,current_user)

'''
class Folha_01Form(ModelForm):
    OPERACAO_CHOICES=(
        ('BRANCO',''),
        ('EXCLUIR','Excluir tramitacao'),
        ('REAGENDAR','Reagendar tramitacao'),
        ('STATUS','Alterar Status'),
        ('INCLUIR','Incluir tramitacoes'),
    )

    operacao = forms.CharField(
        label = 'Operacao',
        widget=forms.Select(choices=OPERACAO_CHOICES),
        max_length=18
        )    

    tramitacao = forms.CharField(
        label = 'Tipo da tramitacao',
        widget=forms.Select(choices=choices.TRAMITACAO),
        max_length=50
        )
    documento = forms.FileField(label='Arquivo Excel')

    def clean_operacao(self):
        operation = self.cleaned_data.get('operacao')
        if(operation=='BRANCO'):
            raise forms.ValidationError("Informe ass operacao")
        return operation
    

    class Meta:
        model = Foha_01
        fields = ('anomes', 'id_setor','id_funcionario','id_provento','valor')


class Leitura_Zip(forms.Form):
    OPERACAO_CHOICES=(
        ('BRANCO',''),
        ('LER','Incluir departamento(s)'),
    )

    operacao = forms.CharField(
        label = 'Operacao',
        widget=forms.Select(choices=OPERACAO_CHOICES),
        max_length=18
        )    

    municipio = forms.CharField(
        label = 'Operacao',
        widget=forms.Select(choices=choices.MUNICIPIOS),
        max_length=18
        )    

    documento = forms.FileField(label='Arquivo Zip')

    def clean_operacao(self):
        operation = self.cleaned_data.get('operacao')
        if(operation=='BRANCO'):
            raise forms.ValidationError("Informe as operacao")
        return operation

class ListagemDepartamento(forms.Form):
    OPERACAO_CHOICES=(
        ('BRANCO',''),
        ('LER','Incluir departamento(s)'),
    )
    municipio = forms.CharField(
        label = 'Tipo da tramitacao',
        widget=forms.Select(choices=choices.MUNICIPIOS),
        max_length=50
        )
'''