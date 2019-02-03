from django.db import models

# Create your models here.

class PA (models.Model):
	stud_id = models.IntegerField(primary_key=True) #Numero nell'elenco
	nome = models.CharField(max_length=200) 
	cognome = models.CharField(max_length=200)

	def __str__(self):
		return str(self.stud_id)+" "+self.nome+" "+self.cognome

	# def __nome__ (self):
	# 	return str(self.nome)
		
	# def __cognome__ (self):
	# 	return str(self.cognome)



class PA_INTERROGAZIONI (models.Model):
	inter_id = models.CharField(max_length=40, primary_key=True) #sha1
	studente = models.ForeignKey(PA, on_delete=models.CASCADE)
	voto = models.CharField(max_length=10)
	nota = models.CharField(max_length=300)
	data = models.DateField()

	def __str__(self):
		return self.inter_id+" "+str(self.studente)+" "+self.voto+" "+str(self.data)+" "+self.nota
	

class PA_GIUSTIFICAZIONI (models.Model):
	giust_id = models.CharField(max_length=40, primary_key=True)
	studente = models.ForeignKey(PA, on_delete=models.CASCADE)
	data = models.DateField()
	nota = models.CharField(max_length=200)
	
	def __str__(self):
		string=self.giustificazione+" "+self.studente+" "+self.data+" "+self.nota
		return string


class PM (models.Model):
	stud_id = models.IntegerField(primary_key=True) #Numero nell'elenco
	nome = models.CharField(max_length=200) 
	cognome = models.CharField(max_length=200)

	def __str__(self):
		string=str(self.stud_id)+" "+self.nome+" "+self.cognome
		return string

class PM_INTERROGAZIONI (models.Model):
	inter_id = models.CharField(max_length=40, primary_key=True) #sha1
	studente = models.ForeignKey(PM, on_delete=models.CASCADE)
	voto = models.CharField(max_length=10)
	nota = models.CharField(max_length=300)
	data = models.DateField()

	def __str__(self):
		string=self.inter_id+" "+self.studente+" "+self.voto+" "+self.data+" "+self.nota
		return string

class PM_GIUSTIFICAZIONI (models.Model):
	giust_id = models.CharField(max_length=40, primary_key=True)
	studente = models.ForeignKey(PM, on_delete=models.CASCADE)
	data = models.DateField()
	nota = models.CharField(max_length=200)

	def __str__(self):
		string=self.giustificazione+" "+self.studente+" "+self.data+" "+self.nota
		return string



