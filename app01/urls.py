from  django.urls import include, path
from django.contrib import admin
from . import views as v1

app_name = 'app01'

urlpatterns = [
    path('lendozip', v1.gerandoFolha_modelo1, name='lendozip'),
    path('deptoList', v1.departamentoList, name='deptoList'),
    path('setorList', v1.setorList, name='setorList'),
    path('listDepSetor', v1.listDepSetor, name='listDepSetor'),
    path('listFolhaResumo', v1.listFolhaResumo, name='listFolhaResumo'),
    path('gravarCSVFolha', v1.gravarCSVFolha, name='gravarCSVFolha'),
    path('importacaoGeral', v1.importacaoGeral, name='importacaoGeral'),

]
