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

Nivel_Programado = (
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Máxima', 'Máxima'),
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

    temperatura = models.FloatField(default=0, null=True)
    humedad = models.FloatField(default=0, null=True)

    temperaturaMax = models.FloatField(default=0, null=True)
    humedadMax = models.FloatField(default=0, null=True)
    horaTMax = models.TimeField(default=timezone.now)
    horaHMax = models.TimeField(default=timezone.now)

    temperaturaMin = models.FloatField(default=100, null=True)
    humedadMin = models.FloatField(default=100, null=True)
    horaTMin = models.TimeField(default=timezone.now)
    horaHMin = models.TimeField(default=timezone.now)
    
    incidencia = models.BooleanField(default=False);

class registroDHT(models.Model):
    
    dht= models.ForeignKey(dht, on_delete=models.CASCADE)
    
    fecha = models.DateField(default=timezone.now)
    
    temperaturaMax = models.FloatField(default=0, null=True)
    humedadMax = models.FloatField(default=0, null=True)
    horaTMax = models.TimeField(default=timezone.now)
    horaHMax = models.TimeField(default=timezone.now)

    temperaturaMin = models.FloatField(default=100, null=True)
    humedadMin = models.FloatField(default=100, null=True)
    horaTMin = models.TimeField(default=timezone.now)
    horaHMin = models.TimeField(default=timezone.now)

class incidenciaDHT(models.Model):
    
    dht= models.ForeignKey(dht, on_delete=models.CASCADE)
    
    fecha = models.DateField(default=timezone.now)
    
    temperatura = models.FloatField(default=0, null=True)
    humedad = models.FloatField(default=0, null=True)
    hora = models.TimeField(default=timezone.now)

class rfid(Modulo):
    uid = models.CharField(default=None, null=True, max_length= 50)
    lastUID = models.CharField(default=None, null=True, max_length= 50)

class registroRFID(models.Model):
    
    rfid= models.ForeignKey(rfid, on_delete=models.CASCADE)
    
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    uid = models.CharField(default=None, null=True, max_length= 50)



class mq2(Modulo):
    lpg = models.FloatField(default=0, null=True);
    co2 = models.FloatField(default=0, null=True);
    smoke = models.FloatField(default=0, null=True);
        
    lpgMax = models.FloatField(default=0, null=True)
    co2Max = models.FloatField(default=0, null=True)
    smokeMax = models.FloatField(default=0, null=True)
    horaLPGMax = models.TimeField(default=timezone.now)
    horaCO2Max = models.TimeField(default=timezone.now)
    horaSMOKEMax = models.TimeField(default=timezone.now)
        
    incidencia = models.BooleanField(default=False);

class registroMQ2(models.Model):
    
    mq2= models.ForeignKey(mq2, on_delete=models.CASCADE)
    
    fecha = models.DateField(default=timezone.now)
    
    lpgMax = models.FloatField(default=0, null=True)
    co2Max = models.FloatField(default=0, null=True)
    smokeMax = models.FloatField(default=0, null=True)
    horaLPGMax = models.TimeField(default=timezone.now)
    horaCO2Max = models.TimeField(default=timezone.now)
    horaSMOKEMax = models.TimeField(default=timezone.now)

class incidenciaMQ2(models.Model):
    
    mq2= models.ForeignKey(mq2, on_delete=models.CASCADE)
    
    fecha = models.DateField(default=timezone.now)
    
    lpg = models.FloatField(default=0, null=True)
    co2 = models.FloatField(default=0, null=True)
    smoke = models.FloatField(default=0, null=True)
    hora = models.TimeField(default=timezone.now)
    
class ldr(Modulo):
	luminosidad = models.FloatField(default=0, null=True);

class puerta(Modulo):
	estado = models.BooleanField(default=False);

class led(Modulo):
    nivel = models.IntegerField(default=0, null=True);
    auto = models.BooleanField(default=False);
    horaInicio = models.TimeField(default=timezone.now)
    horaFin = models.TimeField(default=timezone.now)
    autoProgramado = models.BooleanField(default=False);
    flagAuto = models.BooleanField(default=False);
    flagEnvio = models.BooleanField(default=False);
    nivelProgramado = models.CharField(default=None, null=False, max_length=50, choices=Nivel_Programado)
    

class UserProfile(User):
    codigoHogar = models.CharField(default=None, null=True, max_length= 50)
    uid = models.CharField(default=None, null=False, max_length= 50, unique=True)
    dht = models.ManyToManyField(dht, blank=True) #recogera en una lista los modulos de temperatura que pertenecen a un usuario
    rfid = models.ManyToManyField(rfid, blank=True)
    mq2 = models.ManyToManyField(mq2, blank=True)
    ldr = models.ManyToManyField(ldr, blank=True)
    puerta = models.ManyToManyField(puerta, blank=True)
    led = models.ManyToManyField(led, blank=True)
    conectado = models.BooleanField(default=False, null=False);
    ipBroker = models.CharField(default=None, null=True, max_length= 50)

    def __unicode__(self):
    	return self.user.username
