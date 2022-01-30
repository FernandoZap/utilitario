from  django.urls import include, path
from django.contrib import admin
from . import views as v1

app_name = 'app01'

urlpatterns = [
    path('folha_01', v1.v001_folha_01, name='folha_01'),

]
