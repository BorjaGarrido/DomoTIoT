from django.shortcuts import render, render_to_response
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, newDHTSensorForm, newRFIDSensorForm, newDOORSensorForm, newMQ2SensorForm, newLDRSensorForm, newLEDSensorForm
from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
import datetime
import smtplib

# Create your views here.
@login_required(login_url = '/web/login')
def modulo_list(request):
    #dia = datetime.datetime.now().strftime('%d/%m/%Y')
    #hora = datetime.datetime.now().strftime('%H:%M:%S')
    return render(request, 'web/modulo_list.html') #{'hora': hora})

def contacto(request):
    return render(request, 'web/contacto.html')

def acerca(request):
    return render(request, 'web/acerca.html')

def inicio(request):
    return render(request, 'web/inicio.html')

def dhtDetail(request):
    return render(request, 'web/dhtDetail.html')

def rfidDetail(request):
    member = UserProfile.objects.get(username=request.user)
    uid = member.uid
    return render(request, 'web/rfidDetail.html', {'uid': uid})

def mq2Detail(request):
    return render(request, 'web/mq2Detail.html')

def ldrDetail(request):
    return render(request, 'web/ldrDetail.html')

def doorDetail(request):
    return render(request, 'web/doorDetail.html')

def ledDetail(request):
    return render(request, 'web/ledDetail.html')

def registroUsuario(request):
    if request.method == 'POST':
        form = registroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        form = registroForm()
    return render(request, 'web/registro.html', {'form': form})


def SignInView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = request.POST['username']
            passwd = request.POST['password']
            access = authenticate(username=user, password=passwd)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return redirect('/')
                else:
                    return render(request, 'web/inactive.html')
            else:
                return render(request, 'web/nouser.html')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request,'web/login.html', context)

@login_required(login_url='/web/login/')
def SignOutView(request):
    logout(request)
    return redirect('/')

@login_required(login_url = '/web/login')
def newDHTSensor(request):
    if request.method == "POST":
        form = newDHTSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/dhtDetail')
    else:
        form = newDHTSensorForm()
    return render(request, 'web/newDhtSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newRFIDSensor(request):
    if request.method == "POST":
        form = newRFIDSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/rfidDetail')
    else:
        form = newRFIDSensorForm()
    return render(request, 'web/newRfidSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newMQ2Sensor(request):
    if request.method == "POST":
        form = newMQ2SensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/mq2Detail')
    else:
        form = newMQ2SensorForm()
    return render(request, 'web/newMq2Sensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newLDRSensor(request):
    if request.method == "POST":
        form = newLDRSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/ldrDetail')
    else:
        form = newLDRSensorForm()
    return render(request, 'web/newLdrSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newDOORSensor(request):
    if request.method == "POST":
        form = newDOORSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/doorDetail')
    else:
        form = newDOORSensorForm()
    return render(request, 'web/newDoorSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newLEDSensor(request):
    if request.method == "POST":
        form = newLEDSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/web/ledDetail')
    else:
        form = newLEDSensorForm()
    return render(request, 'web/newLedSensor.html', {'form': form})
