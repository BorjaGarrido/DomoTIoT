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
	temperatura = models.IntegerField(default=None, null=True)
	humedad = models.IntegerField(default=None, null=True)

class rfid(Modulo):
	uid = models.CharField(default=None, null=False, max_length= 50)

class mq2(Modulo):
	lpg = models.IntegerField(default=None, null=True);
	co2 = models.IntegerField(default=None, null=True);
	smoke = models.IntegerField(default=None, null=True);

class ldr(Modulo):
	voltaje = models.IntegerField(default=None, null=True);

class puerta(Modulo):
	estado = models.BooleanField(default=False);

class luz(Modulo):
	luminosidad = models.IntegerField(default=0, null=True);