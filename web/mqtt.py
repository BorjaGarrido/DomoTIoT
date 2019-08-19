import paho.mqtt.client as mqtt

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
import paho.mqtt.publish as publish
import time

def on_connect(client, userdata, rc):
    client.subscribe("casa/rfid")

def on_message(client, userdata, msg):
    members = UserProfile.objects.all()
    
    for member in members:
            
            listaRFID = member.rfid.all()
            
            ipBroker = member.ipBroker
            
            for sensor in listaRFID:

                topic = sensor.topic

                #m = subscribe.simple(topic, hostname=ipBroker, retained=False)
                
                men = str(msg.payload)

                men = men.replace("'", "")
                men = men.replace("b", "")
                men = men.replace("UID Tag", "")
                men = men.split(" ")

                mens = str(men[1]+" "+men[2]+" "+men[3]+" "+men[4])
                
                if mens == str(member.uid):

                    sensor.uid = mens

                    sensor.save()
                    member.rfid.add(sensor)
                    
                    memberUser = UserProfile.objects.get(uid=sensor.uid)
                    
                    listaDOOR = memberUser.puerta.all()
                    
                    for door in listaDOOR:
                        
                        if door.habitacion == sensor.habitacion and door.estado == False:
                            
                            publish.single(door.topic, 1, hostname = member.ipBroker)
                            
                            door.estado = True
                            
                            door.save()
                            memberUser.puerta.add(door) 
                            
                        if door.habitacion == sensor.habitacion and door.estado == True:
                            
                            publish.single(door.topic, 0, hostname = member.ipBroker)
                            
                            door.estado = False
                            
                            door.save()
                            memberUser.puerta.add(door) 
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(localhost, 1883, 60)
