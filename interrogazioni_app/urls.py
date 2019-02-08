from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
	path('<str:_classe>/', views.classe, name="classe"),
    path('<str:_classe>/appello/', views.appello, name="appello"),
    path('<str:_classe>/interrogazioni/', views.interrogazioni, name='interrogazioni'),
    path('<str:_classe>/interrogazioni/random', views.random_interrogazione, name='random_interrogazione'),
    path('<str:_classe>/interrogazioni/nuova', views.nuova_interrogazione, name='nuova_interrogazione'),
    path('<str:_classe>/interrogazioni/crea', views.crea_interrogazione, name='crea_interrogazione'),
    path('<str:_classe>/interrogazioni/rimuovi', views.rimuovi_interrogazione, name='rimuovi_interrogazione'),
    path('<str:_classe>/giustificazioni/', views.giustificazioni, name='giustificazioni'),
    path('<str:_classe>/giustificazioni/nuova', views.nuova_giustificazione, name='nuova_giustificazione'),
    path('<str:_classe>/giustificazioni/rimuovi', views.rimuovi_giustificazione, name='rimuovi_giustificazione'),
    path('', views.index, name="index")
]