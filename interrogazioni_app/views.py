from django.shortcuts import render
from django.http import HttpResponse

from interrogazioni_app.models import *
# from django.utils import timezone
from datetime import datetime, date

import os
import hashlib

# from FillDB import *

def index (request):
	return render(request, "home.html")

def classe(request, _classe):
	context ={
		"classe" : _classe,
	}
	return render(request, "home_classe.html", context)

def generic(request, _classe, _interr, _giust):
	classe=None
	voti=None
	giustificazioni=None
	if _classe=="PA": #scegli la classe
		classe=PA
		voti=PA_INTERROGAZIONI if _interr else None
		giustificazioni=PA_GIUSTIFICAZIONI if _giust else None
	else:
		classe=PM
		voti=PM_INTERROGAZIONI if _interr else None
		giustificazioni=PM_GIUSTIFICAZIONI if _giust else None

	lista=classe.objects.all() #Prendi tutti gli alunni nella classe
	lista_voti=voti.objects.all() if voti else [] #Prendi tutti i voti degli alunni
	lista_giust=giustificazioni.objects.all() if giustificazioni else [] #Prendi tutte le giustificazioni degli alunni

	date=[] #Prendi tutte le date
	if (_interr):
		for interrogazione in lista_voti:
			if not (interrogazione.data in date):
				date.append(interrogazione.data)
	if (_giust):
		for giustificazione in lista_giust:
			if not (giustificazione.data in date):
				date.append(giustificazione.data)

	#Crea una matrice con tante colonne quante le date + id, nome, cognome e tante righe quanti gli alunni
	matrice=[[0 for y in range(len(date)+3) ] for x in range(len(lista))] #date+id+nome+cognome

	for x in range(len(lista)):
		#Inserisci id, nome, cognome nella matrice	
		matrice[x][0]=lista[x].stud_id
		matrice[x][1]=lista[x].nome
		matrice[x][2]=lista[x].cognome
		for y in range (len(date)):
			for giust in lista_giust: #Inserisci la giustificazione solo se l'id e la data dello studente combaciano
				if giust.studente.stud_id==lista[x].stud_id and giust.data==date[y]:
					matrice[x][3+y]="G" 
				else: #Se è già presente un voto, non sovrascriverlo con uno spazio vuoto
					matrice[x][3+y]="" if matrice[x][3+y]==0 else matrice[x][3+y]
			for voto in lista_voti: #Inserisci i voti solo se l'id e la data dello studente combaciano
				if voto.studente.stud_id==lista[x].stud_id and voto.data==date[y]:
					matrice[x][3+y]=voto.voto
				else: #Se è già presente un voto, non sovrascriverlo con uno spazio vuoto
					matrice[x][3+y]="" if matrice[x][3+y]==0 else matrice[x][3+y]

	return [matrice, date]


def appello(request, _classe):
	[matrice, date]=generic(request, _classe, True, False)
	context={
		"classe": ("1A" if _classe=="PA" else "1M"),
		"date" : date,
		"matrice" : matrice,
	}
	return render(request, "app_inter_giust.html", context)

def interrogazioni (request, _classe):
	[matrice, date] = generic(request, _classe, True, False)
	context={
		"classe": ("1A" if _classe=="PA" else "1M"),
		"date" : date,
		"matrice" : matrice,
	}
	return render(request, "app_inter_giust.html", context)

def giustificazioni (request, _classe):
	[matrice, date] = generic(request, _classe, False, True)
	context={
		"classe": ("1A" if _classe=="PA" else "1M"),
		"date" : date,
		"matrice" : matrice,
	}
	return render(request, "app_inter_giust.html", context)


def nuova_generic (request, _classe, _interr, _giust):
	classe=PA if _classe=="PA" else PM
	if (_interr):
		classe_interr=PA_INTERROGAZIONI if _classe=="PA" else PM_INTERROGAZIONI
	elif (_giust):
		classe_giust=PA_GIUSTIFICAZIONI if _classe=="PA" else PM_GIUSTIFICAZIONI
	else:
		return HttpResponse("400 Qualcosa è andato storto")

	_stud_id=request.GET.get('stud_id') #Deve esserci almeno lo stud_id
	if not(_stud_id):
		return HttpResponse("400 Manca l'id dello studente.")
	_nome=request.GET.get('nome') if request.GET.get('nome') else ""
	_cognome=request.GET.get('cognome') if request.GET.get('cognome') else ""

	try: #Prendi tutti gli studenti
		_studente = classe.objects.get(stud_id=int(_stud_id))
	except Exception as e:
		return HttpResponse("404 Studente non trovato")
	# print(_studente)
	if ((	_studente.nome!=_nome and _nome!="") or 
				_studente.cognome!=_cognome and _cognome!=""): #se sono definiti _nome e _cognome controlla che stud_id sia corretto
		return HttpResponse("400 Studente sbagliato.")

	if _interr:
		_voto=request.GET.get('voto') #Ci deve essere un voto
		if not(_voto):
			return HttpResponse("400 Manca il voto.")

	_nota=request.GET.get('nota') if request.GET.get('nota') else ""
	_data=request.GET.get('data') if request.GET.get('data') else datetime.now().strftime("%Y-%m-%d") 
	#+"-"+_data_.strftime("%m")+"-"+_data_.strftime("%d")
	#l'inter_id è dato da stud_id+_data in sha1
	_id= hashlib.sha1((_stud_id+str(_data)).encode('utf-8')).hexdigest()

	nuovo=None
	if (_interr):
		nuovo=classe_interr(	inter_id=_id, studente=_studente, 
																	voto=_voto, nota=_nota, data=_data)
	elif (_giust):
		nuovo=classe_giust(	giust_id=_id, studente=_studente,
																	data=_data, nota=_nota)
	else:
		return HttpResponse("400 Come ci sei arrivato qua?")

	return nuovo

def nuova_interrogazione(request, _classe):
	[interrogazione, errore]=nuova_generic(request, _classe, True, False)
	if errore:
		return HttpResponse(errore)
	else:
		interrogazione.save()

		context={
			"interrogazione": interrogazione,
			"classe" : _classe
		}
		return render(request, "modifica_interrogazione.html", context)

# def nuova_interrogazione (request, _classe):
# 	classe=PA if _classe=="PA" else PM
# 	classe_interr=PA_INTERROGAZIONI if _classe=="PA" else PM_INTERROGAZIONI

# 	_stud_id=request.GET.get('stud_id') #Deve esserci almeno lo stud_id
# 	if not(_stud_id):
# 		return HttpResponse("400 Manca l'id dello studente.")
# 	_nome=request.GET.get('nome') if request.GET.get('nome') else ""
# 	_cognome=request.GET.get('cognome') if request.GET.get('cognome') else ""

# 	try: #Prendi tutti gli studenti
# 		_studente = classe.objects.get(stud_id=int(_stud_id))
# 	except Exception as e:
# 		return HttpResponse("404 Studente non trovato")
# 	# print(_studente)
# 	if ((	_studente.nome!=_nome and _nome!="") or 
# 				_studente.cognome!=_cognome and _cognome!=""): #se sono definiti _nome e _cognome controlla che stud_id sia corretto
# 		return HttpResponse("400 Studente sbagliato.")

# 	_voto=request.GET.get('voto') #Ci deve essere un voto
# 	if not(_voto):
# 		return HttpResponse("400 Manca il voto.")

# 	_nota=request.GET.get('nota') if request.GET.get('nota') else ""
# 	_data_=datetime.now() 
# 	_data=_data_.strftime("%Y")+"-"+_data_.strftime("%m")+"-"+_data_.strftime("%d")
# 	#l'inter_id è dato da stud_id+_data in sha1
# 	_inter_id= hashlib.sha1((_stud_id+str(_data)).encode('utf-8')).hexdigest()

# 	interrogazione=classe_interr(	inter_id=_inter_id, studente=_studente, 
# 																voto=_voto, nota=_nota, data=_data)
# 	interrogazione.save()
# 	context={
# 		"classe" : _classe,
# 		"interrogazione" : interrogazione,
# 	}
# 	return render(request, "modifica_interrogazione.html", context)

def rimuovi_interrogazione (request, _classe):
	classe=PA if _classe=="PA" else PM
	classe_interr=PA_INTERROGAZIONI if _classe=="PA" else PM_INTERROGAZIONI

	_inter_id=request.GET.get('inter_id')
	_stud_id=request.GET.get('stud_id') 
	_data=request.GET.get('data')

	if _inter_id:
		try: #Trova l'interrogazione
			interrogazione = classe.objects.get(inter_id=_inter_id)
		except Exception as e:
			return HttpResponse("404 Interrogazione non trovata")

	elif _stud_id and _data:
		_data=datetime.strptime(_data, '%Y-%m-%d').date()
		try: #Trova l'interrogazione
			try: #Trova lo studente per poter trovare l'interrogazione
				_studente = classe.objects.get(stud_id=_stud_id)
			except Exception as e:
				return HttpResponse("404 Studente non trovato")
			interrogazione = classe_interr.objects.get(studente=_studente, data=_data)
		except Exception as e:
			return HttpResponse("404 Interrogazione non trovata")
	
	else:		
		return HttpResponse("400 Necessario id dell'interrogazione oppure id dello studente e data dell'interrogazione.")
	#Elimina l'interrogazione
	context ={
		"interrogazione" : interrogazione,
		"classe" : _classe,
	}
	interrogazione.delete()
	return render(request, "modifica_interrogazione.html", context)

def nuova_giustificazione(request, _classe):
	[giustificazione, errore]=nuova_generic(request, _classe, False, True)
	if errore:
		return HttpResponse(errore)
	else:
		giustificazione.save()

		context={
			"giustificazione": giustificazione,
			"classe" : _classe
		}
		return render(request, "modifica_giustificazione.html", context)

def rimuovi_giustificazione(request, _classe):
	pass

