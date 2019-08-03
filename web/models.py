from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from uuid import uuid4
# Create your models here.

Tipo_Modulo = (
        ('rfid', 'rfid'),
        ('dht', 'dht'),
        ('mq2', 'mq2'),
        ('ldr', 'ldr'),
        ('led', 'led'),
        ('puerta', 'puerta'),
    )


class Modulo(models.Model):
    nombre = models.CharField(default=None, null=False, max_length= 50, unique=True)
    descripcion= models.CharField(default=None, null=False, max_length= 250)
    habitacion =  models.CharField(default=None, null=False, max_length= 250)
    topic=models.CharField(default=None, null=False, max_length= 50, unique=True)
    tipo = models.CharField(default=None, null=False, max_length=50, choices=Tipo_Modulo)
    codigoHogar = models.CharField(default=None, null=True, max_length= 50)

    def __unicode__(self):
    	return self.nombre

class dht(Modulo):

    temperatura = models.FloatField(default=None, null=True)
    humedad = models.FloatField(default=None, null=True)

    temperaturaMax = models.FloatField(default=None, null=True)
    humedadMax = models.FloatField(default=None, null=True)
    fechaTMax = models.DateField(default=timezone.now)
    fechaHMax = models.DateField(default=timezone.now)
    horaTMax = models.TimeField(default=timezone.now)
    horaHMax = models.TimeField(default=timezone.now)

    temperaturaMin = models.FloatField(default=None, null=True)
    humedadMin = models.FloatField(default=None, null=True)
    fechaTMin = models.DateField(default=timezone.now)
    fechaHMin = models.DateField(default=timezone.now)
    horaTMin = models.TimeField(default=timezone.now)
    horaHMin = models.TimeField(default=timezone.now)

class rfid(Modulo):
	uid = models.CharField(default=None, null=True, max_length= 50)

class mq2(Modulo):
	lpg = models.FloatField(default=None, null=True);
	co2 = models.FloatField(default=None, null=True);
	smoke = models.FloatField(default=None, null=True);

class ldr(Modulo):
	luminosidad = models.FloatField(default=None, null=True);

class puerta(Modulo):
	estado = models.BooleanField(default=False);

class led(Modulo):
	nivel = models.IntegerField(default=0, null=True);

class UserProfile(User):
    codigoHogar = models.CharField(default=None, null=True, max_length= 50)
    uid = models.CharField(default=None, null=False, max_length= 50, unique=True)
    dht = models.ManyToManyField(dht, blank=True) #recogera en una lista los modulos de temperatura que pertenecen a un usuario
    rfid = models.ManyToManyField(rfid, blank=True)
    mq2 = models.ManyToManyField(mq2, blank=True)
    ldr = models.ManyToManyField(ldr, blank=True)
    puerta = models.ManyToManyField(puerta, blank=True)
    led = models.ManyToManyField(led, blank=True)

    def __unicode__(self):
    	return self.user.username
