from django.db import models

from django.utils import timezone

# Create your models here.

class Modulo(models.Model):
	nombre = models.CharField(default=None, null=False, max_length= 50)
	numero = models.IntegerField(default=None)
	descripcion= models.CharField(default=None, null=False, max_length= 250)
	topic=models.CharField(default=None, null=False, max_length= 50)
	fecha = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return self.nombre

class dht(Modulo):
	grados = models.IntegerField(default=None, null=True)
	humedad = models.IntegerField(default=None, null=True)

