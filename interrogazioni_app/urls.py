from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
		path('<str:_classe>/', views.classe, name="classe"),
    path('appello/<str:_classe>/', views.appello, name="appello"),
    path('interrogazioni/<str:_classe>/', views.interrogazioni, name='interrogazioni'),
    path('interrogazioni/<str:_classe>/nuova/', views.nuova_interrogazione, name='nuova_interrogazione'),
    path('interrogazioni/<str:_classe>/rimuovi/', views.rimuovi_interrogazione, name='rimuovi_interrogazione'),
    path('giustificazioni/<str:_classe>/', views.giustificazioni, name='giustificazioni'),
    path('giustificazioni/<str:_classe>/nuova/', views.nuova_giustificazione, name='nuova_giustificazione'),
    path('giustificazioni/<str:_classe>/rimuovi/', views.rimuovi_giustificazione, name='rimuovi_giustificazione'),
    path('', views.index, name="index")
]