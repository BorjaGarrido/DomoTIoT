from __future__ import absolute_import 
from celery import shared_task

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, editUserForm
from .forms import  addSensorForm, newSensorForm, editSensorForm
from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led
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


@shared_task 
def add(x, y): 
    return x + y

@shared_task 
def mul(x, y): 
    return x * y

@shared_task 
def xsum(numbers): 
    return sum(numbers)

@shared_task 
def dhtData(): 
    
    members = UserProfile.objects.all()
    
    for member in members:
        
        if member.conectado == True:
            
            listaDHT = member.dht.all()
            
            for sensor in listaDHT:

                topic = sensor.topic

                m = subscribe.simple(topic, hostname="192.168.1.143", retained=False)

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
                    sensor.fechaTMax = datetime.now()
                    sensor.horaTMax = datetime.now()

                if sensor.humedad > sensor.humedadMax:
                    sensor.humedadMax = sensor.humedad
                    sensor.fechaHMax = datetime.now()
                    sensor.horaHMax = datetime.now()

                if sensor.temperatura < sensor.temperaturaMin:
                    sensor.temperaturaMin = sensor.temperatura
                    sensor.fechaTMin = datetime.now()
                    sensor.horaTMin = datetime.now()

                if sensor.humedad < sensor.humedadMin:
                    sensor.humedadMin = sensor.humedad
                    sensor.fechaHMin = datetime.now()
                    sensor.horaHMin = datetime.now()

                sensor.save()
                member.dht.add(sensor)
        
    return 
