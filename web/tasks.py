from __future__ import absolute_import 
from celery import shared_task

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, editUserForm
from .forms import  addSensorForm, newSensorForm, editSensorForm
from .models import Modulo, UserProfile
from .models import dht, rfid, mq2, ldr, puerta, led
from .models import registroDHT, incidenciaDHT
from .models import registroMQ2, incidenciaMQ2, registroRFID
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from datetime import datetime
from django.utils import timezone
from .tasks import *
import smtplib
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template import RequestContext

@shared_task 
def sensorData(): 
    
    members = UserProfile.objects.all()
    
    for member in members:
            
            listaDHT = member.dht.all()
            
            listaMQ2 = member.mq2.all()
            
            listaLDR = member.ldr.all()
                
            listaLED = member.led.all()
            
            ipBroker = member.ipBroker
            
            for sensor in listaDHT:

                topic = sensor.topic

                m = subscribe.simple(topic, hostname=ipBroker, retained=False)

                men = str(m.payload)
                men = men.replace("'", "")
                men = men.replace("b", "")
                men = men.replace("Hum", "")
                men = men.replace("Temp", "")
                men = men.split(" ")

                sensor.temperatura = float(men[3])
                sensor.humedad = float(men[1])

                if sensor.temperatura > sensor.temperaturaMax:
                    sensor.temperaturaMax = sensor.temperatura
                    sensor.horaTMax = datetime.now()

                if sensor.humedad > sensor.humedadMax:
                    sensor.humedadMax = sensor.humedad
                    sensor.horaHMax = datetime.now()

                if sensor.temperatura < sensor.temperaturaMin:
                    sensor.temperaturaMin = sensor.temperatura
                    sensor.horaTMin = datetime.now()

                if sensor.humedad < sensor.humedadMin:
                    sensor.humedadMin = sensor.humedad
                    sensor.horaHMin = datetime.now()

                sensor.save()
                member.dht.add(sensor)
         
            for sensor in listaMQ2:

                    topic = sensor.topic

                    m = subscribe.simple(topic, hostname=ipBroker, retained=False)
                    
                    men = str(m.payload)
                    men = men.replace("'", "")
                    men = men.replace("b", "")
                    men = men.replace("\\t", "")
                    men = men.replace("LPG", "")
                    men = men.replace("CO", "")
                    men = men.replace("SMOKE", "")
                    men = men.split(" ")

                    sensor.lpg = float(men[1])
                    sensor.co2 = float(men[3])
                    sensor.smoke = float(men[6])
                    
                    if sensor.lpg > sensor.lpgMax:
                        sensor.lpgMax = sensor.lpg
                        sensor.horaLPGMax = datetime.now()

                    elif sensor.co2 > sensor.co2Max:
                        sensor.co2Max = sensor.co2
                        sensor.horaCO2Max = datetime.now()

                    elif sensor.smoke > sensor.smokeMax:
                        sensor.smokeMax = sensor.smoke
                        sensor.horaSMOKEMax = datetime.now()

                    sensor.save()
                    member.mq2.add(sensor)
                
            for sensor in listaLDR:

                    topic = sensor.topic

                    m = subscribe.simple(topic, hostname=ipBroker, retained=False)
                    
                    men = str(m.payload)

                    men = men.replace("'", "")
                    men = men.replace("b", "")
                    men = men.replace("Vol", "")
                    men = men.split(" ")

                    sensor.luminosidad = float(men[1])
                    
                    for led in listaLED:
                        
                        if sensor.habitacion == led.habitacion and led.auto == True:
                            
                            if sensor.luminosidad > 3.5:
                                
                                led.nivel = 0
                                publish.single(led.topic, 0, hostname = member.ipBroker)
                            
                            elif sensor.luminosidad <= 3.5 and sensor.luminosidad > 2:
                            
                                led.nivel = 124
                                publish.single(led.topic, 124, hostname = member.ipBroker)
                            
                            elif sensor.luminosidad <= 2 and sensor.luminosidad > 1:
                            
                                led.nivel = 512
                                publish.single(led.topic, 512, hostname = member.ipBroker)
                            
                            elif sensor.luminosidad <= 1 and sensor.luminosidad >= 0:
                            
                                led.nivel = 1024
                                publish.single(led.topic, 1024, hostname = member.ipBroker)
                            
                            led.save()
                            member.led.add(led)
                            
                    
                    sensor.save()
                    member.ldr.add(sensor)
            
    return 

@shared_task 
def autoProgramLed(): 
    
    members = UserProfile.objects.all()
    
    hora_act = datetime.now().time()
    
    for member in members:
            
            listaLED = member.led.all()
            
            for led in listaLED:
                
                nivelGuardado = led.nivel

                if led.autoProgramado == True:

                    horaInicio = led.horaInicio
                    horaFin = led.horaFin 
                    
                    if horaInicio < hora_act and hora_act < horaFin:
                            
                            if led.auto == True:
                            
                                led.auto = False
                                led.flagAuto = True
                            
                            if led.nivelProgramado == "Baja":
                                led.nivel = 124
                            elif led.nivelProgramado == "Media":
                                led.nivel = 512
                            elif led.nivelProgramado == "Máxima":
                                led.nivel = 1024
                            
                            led.flagEnvio = True
                            
                            led.save()
                            member.led.add(led)    
                            
                            publish.single(led.topic, led.nivel, hostname = member.ipBroker)
                        
                    else:
                        
                        if led.flagEnvio == True:
                        
                            led.nivel = 0
                                
                            publish.single(led.topic, 0, hostname = member.ipBroker)    
                                
                            if led.flagAuto == True:
                                
                                led.flagAuto = False
                                led.auto = True
                            
                            led.flagEnvio = False
                                        
                            led.save()
                            member.led.add(led)
                            
    return 



@shared_task 
def rfidData(): 
    
    members = UserProfile.objects.all()
    
    bandera = True
    
    for member in members:
            
            listaRFID = member.rfid.all()
            
            ipBroker = member.ipBroker
            
            for sensor in listaRFID:

                topic = sensor.topic

                m = subscribe.simple(topic, hostname=ipBroker, retained=False)
                
                men = str(m.payload)

                men = men.replace("'", "")
                men = men.replace("b", "")
                men = men.replace("UID Tag", "")
                men = men.split(" ")

                mens = str(men[1]+" "+men[2]+" "+men[3]+" "+men[4])
                
                if mens == str(member.uid):

                    sensor.uid = mens

                    sensor.save()
                    member.rfid.add(sensor)
                    
    return  

@shared_task 
def puertaOpen(): 
    
    members = UserProfile.objects.all()
    
    bandera = True
    
    for member in members:
            
            listaRFID = member.rfid.all()
            
            ipBroker = member.ipBroker
            
            for sensor in listaRFID:

                memberUser = UserProfile.objects.get(uid=sensor.uid)
                        
                listaDOOR = memberUser.puerta.all()
                        
                for door in listaDOOR:
                    
                    if door.habitacion == sensor.habitacion and door.estado == False:
                                
                        if bandera == True:
                                
                            publish.single(door.topic, 1, hostname = member.ipBroker)
                                    
                            door.estado = True
                                
                            door.save()
                            memberUser.puerta.add(door) 
                                
                            bandera = False
                            bandera2 = True
                                    
                            if bandera2 == True:
                                    
                                time.sleep(5)
                                        
                                publish.single(door.topic, 0, hostname = member.ipBroker)
                                        
                                door.estado = False
                                        
                                door.save()
                                memberUser.puerta.add(door) 
                                        
                                bandera2 = False
                        
                        registro = registroRFID.objects.create(rfid=sensor,
                                        fecha = datetime.now().date(),
                                        hora = datetime.now().time(),
                                        uid = sensor.uid,)  
                        
                        registro.save()
                        
                        sensor.uid = None
                        
                        sensor.save()
                        memberUser.rfid.add(sensor)
                        
                        
    
    
    return 

@shared_task 
def registros(): 
    
    members = UserProfile.objects.all()
    
    for member in members:
            
            listaDHT = member.dht.all()
            listaMQ2 = member.mq2.all()
            fechaR = datetime.now().date()
            
            for sensor in listaDHT:
                
                temperaturaMaxi = sensor.temperaturaMax
                humedadMaxi = sensor.humedadMax
                horaTMaxi = sensor.horaTMax 
                horaHMaxi = sensor.horaHMax

                temperaturaMini = sensor.temperaturaMin
                humedadMini = sensor.humedadMin
                horaTMini = sensor.horaTMin
                horaHMini = sensor.horaHMin
                
                registro = registroDHT.objects.create(dht=sensor,
                    fecha = fechaR,
                
                    temperaturaMax = temperaturaMaxi,
                    humedadMax = humedadMaxi,
                    horaTMax = horaTMaxi,
                    horaHMax = horaHMaxi,

                    temperaturaMin = temperaturaMini,
                    humedadMin = humedadMini,
                    horaTMin = horaTMini,
                    horaHMin = horaHMini,)
                
                registro.save()
                
                sensor.temperaturaMax = 0
                sensor.humedadMax = 0
                
                sensor.temperaturaMin = 100
                sensor.humedadMin = 100

                sensor.save()
                member.dht.add(sensor)
            
            for sensor in listaMQ2:
                
                lpg = sensor.lpgMax
                co2 = sensor.co2Max
                smoke = sensor.smokeMax
                
                horal = sensor.horaLPGMax
                horac = sensor.horaCO2Max 
                horas = sensor.horaSMOKEMax
                
                registro = registroMQ2.objects.create(mq2=sensor,
                    fecha = fechaR,
                
                    lpgMax = lpg,
                    co2Max = co2,
                    smokeTMax = smoke,
                    horaLPGMax = horal,
                    horaCO2Max = horac,
                    horaSMOKEMax = horas,)
                
                registro.save()
                
                sensor.lpgMax = 0
                sensor.co2Max = 0 
                sensor.smokeMax = 0

                sensor.save()
                member.mq2.add(sensor)
        
    return 

@shared_task 
def incidencias(): 
    
    members = UserProfile.objects.all()
    
    for member in members:
            
            listaDHT = member.dht.all()
            listaMQ2 = member.mq2.all()
            
            for sensor in listaDHT:

                temperatura = sensor.temperatura
                humedad = sensor.humedad
                
                hora  = datetime.now().time()
                fecha = datetime.now().date()
                
                if sensor.incidencia == False:
                    
                    if sensor.humedad > 85 and sensor.temperatura > 45:

                        #render_to_string permite renderizar un html en un string
                        body = render_to_string('web/humTempAlta.html',
                            {'humedad': humedad,
                             'fecha': fecha,
                             'hora': hora,
                             'temperatura': temperatura,
                            })
                        
                        #Se envía el email con el string renderizado anteriormente
                        email_message = EmailMessage(
                            subject='PELIGRO',
                            body=body,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[member.email],
                        )
                        
                        email_message.content_subtype = 'html'
                        email_message.send()
                        
                        incidencia = incidenciaDHT.objects.create(dht=sensor,
                            temperatura = temperatura,
                            humedad = humedad,
                            hora = hora,
                            fecha = fecha,)
                
                        incidencia.save()
                
                        sensor.incidencia = True

                        sensor.save()
                        member.dht.add(sensor)
                    
                    elif sensor.temperatura > 45:

                        #render_to_string permite renderizar un html en un string
                        body = render_to_string('web/temperaturaAlta.html',
                            {'temperatura': temperatura,
                             'fecha': fecha,
                             'hora': hora,
                            })
                        
                        #Se envía el email con el string renderizado anteriormente
                        email_message = EmailMessage(
                            subject='PELIGRO',
                            body=body,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[member.email],
                        )
                        
                        email_message.content_subtype = 'html'
                        email_message.send()
                        
                        incidencia = incidenciaDHT.objects.create(dht=sensor,
                            temperatura = temperatura,
                            humedad = humedad,
                            hora = hora,
                            fecha = fecha,)
                
                        incidencia.save()
                
                        sensor.incidencia = True

                        sensor.save()
                        member.dht.add(sensor)
                        
                    elif sensor.humedad > 85:

                        #render_to_string permite renderizar un html en un string
                        body = render_to_string('web/humedadAlta.html',
                            {'humedad': humedad,
                             'fecha': fecha,
                             'hora': hora,
                            })
                        
                        #Se envía el email con el string renderizado anteriormente
                        email_message = EmailMessage(
                            subject='Aviso',
                            body=body,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[member.email],
                        )
                        
                        email_message.content_subtype = 'html'
                        email_message.send()
                        
                        incidencia = incidenciaDHT.objects.create(dht=sensor,
                            temperatura = temperatura,
                            humedad = humedad,
                            hora = hora,
                            fecha = fecha,)
                
                        incidencia.save()
                
                        sensor.incidencia = True

                        sensor.save()
                        member.dht.add(sensor)
                        
            for sensor in listaMQ2:

                lpg = sensor.lpg
                co2 = sensor.co2
                smoke = sensor.smoke
                
                hora  = datetime.now().time()
                fecha = datetime.now().date()
                
                if sensor.incidencia == False:
                    
                    if sensor.lpg > 2 or sensor.co2 > 0 or sensor.smoke > 6:
                        
                        #render_to_string permite renderizar un html en un string
                        body = render_to_string('web/gasAlto.html',
                            {'lpg': lpg,
                             'co2': co2,
                             'smoke': smoke,
                             'hora': hora,
                             'fecha': fecha,
                            })
                        
                        #Se envía el email con el string renderizado anteriormente
                        email_message = EmailMessage(
                            subject='PELIGRO',
                            body=body,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[member.email],
                        )
                        
                        email_message.content_subtype = 'html'
                        email_message.send()
                        
                        incidencia = incidenciaMQ2.objects.create(mq2=sensor,
                            lpg = lpg,
                            co2 = co2,
                            smoke = smoke,
                            hora = hora,
                            fecha = fecha,)
                
                        incidencia.save()
                
                        sensor.incidencia = True

                        sensor.save()
                        member.mq2.add(sensor)
                
                

    return 
   
@shared_task 
def reiniciarIncidencias(): 
    
    members = UserProfile.objects.all()
    
    for member in members:
            
            listaDHT = member.dht.all()
            listaMQ2 = member.mq2.all()
            
            for sensor in listaDHT:

                if sensor.incidencia == True:
                    
                    sensor.incidencia = False
                    
                    sensor.save()
                    member.dht.add(sensor)

            for sensor in listaMQ2:

                if sensor.incidencia == True:
                    
                    sensor.incidencia = False
                    
                    sensor.save()
                    member.mq2.add(sensor)
    return
