from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, newDHTSensorForm, newRFIDSensorForm, newDOORSensorForm, newMQ2SensorForm, newLDRSensorForm, newLEDSensorForm, editUserForm, addSensorForm
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
from django.db.models import Q
from django.shortcuts import redirect
import datetime
import smtplib

# Create your views here.
@login_required(login_url = '/web/login')
def modulo_list(request):
    return render(request, 'web/modulo_list.html')

def contacto(request):
    return render(request, 'web/contacto.html')

def acerca(request):
    return render(request, 'web/acerca.html')

def inicio(request):
    return render(request, 'web/inicio.html')

def dhtDetail(request):
    return render(request, 'web/dhtDetail.html')

def rfidDetail(request):
    return render(request, 'web/rfidDetail.html')

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

def userDetail(request):
    member = request.user.userprofile
    nombre = member.first_name
    apellido = member.last_name
    username = member.username
    uid = member.uid
    codigoHogar = member.codigoHogar
    email = member.email
    return render(request, 'web/userDetail.html', {'nombre': nombre, 'apellido': apellido, 'username': username, 'uid': uid, 'codigoHogar': codigoHogar, 'email': email})

@login_required(login_url='/web/login/')
def editUser(request):
    if request.method == 'POST':
        form = editUserForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('/web/userDetail')
    else:
        form = editUserForm(instance=request.user.userprofile)
        return render(request, 'web/editUserForm.html', {'form': form})

@login_required(login_url='/web/login/')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'web/changePasswordForm.html', {'form': form})

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
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.dht.add(post)
            return redirect('/web/dhtDetail')
    else:
        form = newDHTSensorForm()
    return render(request, 'web/newDhtSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addDHTSensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if dht.objects.filter(nombre=nombre).exists():
                sensor = dht.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.dht.add(sensor)
                return redirect('/web/dhtDetail')
            else:
                messages.error(request, '*Sensor DHT no encontrado')
                return redirect('/web/addDhtSensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addDhtSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newRFIDSensor(request):
    if request.method == "POST":
        form = newRFIDSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.rfid.add(post)
            return redirect('/web/rfidDetail')
    else:
        form = newRFIDSensorForm()
    return render(request, 'web/newRfidSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addRFIDSensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if rfid.objects.filter(nombre=nombre).exists():
                sensor = rfid.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.rfid.add(sensor)
                return redirect('/web/rfidDetail')
            else:
                messages.error(request, '*Sensor RFID no encontrado')
                return redirect('/web/addRfidSensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addRfidSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newMQ2Sensor(request):
    if request.method == "POST":
        form = newMQ2SensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.mq2.add(post)
            return redirect('/web/mq2Detail')
    else:
        form = newMQ2SensorForm()
    return render(request, 'web/newMq2Sensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addMQ2Sensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if mq2.objects.filter(nombre=nombre).exists():
                sensor = mq2.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.mq2.add(sensor)
                return redirect('/web/mq2Detail')
            else:
                messages.error(request, '*Sensor MQ2 no encontrado')
                return redirect('/web/addMq2Sensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addMq2Sensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newLDRSensor(request):
    if request.method == "POST":
        form = newLDRSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.ldr.add(post)
            return redirect('/web/ldrDetail')
    else:
        form = newLDRSensorForm()
    return render(request, 'web/newLdrSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addLDRSensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if ldr.objects.filter(nombre=nombre).exists():
                sensor = ldr.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.ldr.add(sensor)
                return redirect('/web/ldrDetail')
            else:
                messages.error(request, '*Sensor LDR no encontrado')
                return redirect('/web/addLdrSensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addLdrSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newDOORSensor(request):
    if request.method == "POST":
        form = newDOORSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.puerta.add(post)
            return redirect('/web/doorDetail')
    else:
        form = newDOORSensorForm()
    return render(request, 'web/newDoorSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addDOORSensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if puerta.objects.filter(nombre=nombre).exists():
                sensor = puerta.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.puerta.add(sensor)
                return redirect('/web/doorDetail')
            else:
                messages.error(request, '*Sensor DOOR no encontrado')
                return redirect('/web/addDoorSensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addDoorSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def newLEDSensor(request):
    if request.method == "POST":
        form = newLEDSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            member = request.user.userprofile
            post.codigoHogar = member.codigoHogar
            post.save()
            member.led.add(post)
            return redirect('/web/ledDetail')
    else:
        form = newLEDSensorForm()
    return render(request, 'web/newLedSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addLEDSensor(request):
    form = addSensorForm()
    if request.method == "POST":
        form = addSensorForm(request.POST)
        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre')
            if led.objects.filter(nombre=nombre).exists():
                sensor = led.objects.get(nombre=nombre)
                member = request.user.userprofile
                if sensor.codigoHogar == member.codigoHogar:
                    member.led.add(sensor)
                return redirect('/web/ledDetail')
            else:
                messages.error(request, '*Sensor LED no encontrado')
                return redirect('/web/addLedSensor')
    else:
        form = addSensorForm()
    return render(request, 'web/addLedSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def dhtSensor_list(request):
    member = request.user.userprofile
    lista = member.dht.all()
    return render(request, 'web/listDHT.html', {'lista':lista})

@login_required(login_url = '/web/login')
def rfidSensor_list(request):
    member = request.user.userprofile
    lista = member.rfid.all()
    return render(request, 'web/listRFID.html', {'lista':lista})

@login_required(login_url = '/web/login')
def mq2Sensor_list(request):
    member = request.user.userprofile
    lista = member.mq2.all()
    return render(request, 'web/listMQ2.html', {'lista':lista})

@login_required(login_url = '/web/login')
def doorSensor_list(request):
    member = request.user.userprofile
    lista = member.puerta.all()
    return render(request, 'web/listDOOR.html', {'lista':lista})

@login_required(login_url = '/web/login')
def ldrSensor_list(request):
    member = request.user.userprofile
    lista = member.ldr.all()
    return render(request, 'web/listLDR.html', {'lista':lista})

@login_required(login_url = '/web/login')
def ledSensor_list(request):
    member = request.user.userprofile
    lista = member.led.all()
    return render(request, 'web/listLED.html', {'lista':lista})

@login_required(login_url = '/web/login')
def dht_edit(request, dht_id):
        post = get_object_or_404(dht, pk=dht_id)
        if request.method == "POST":
            form = newDHTSensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.dht.add(post)
                return redirect('/web/listDHT')
        else:
            form = newDHTSensorForm(instance=post)
        return render(request, 'web/dht_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def mq2_edit(request, mq2_id):
        post = get_object_or_404(mq2, pk=mq2_id)
        if request.method == "POST":
            form = newMQ2SensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.mq2.add(post)
                return redirect('/web/listMQ2')
        else:
            form = newMQ2SensorForm(instance=post)
        return render(request, 'web/mq2_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def rfid_edit(request, rfid_id):
        post = get_object_or_404(rfid, pk=rfid_id)
        if request.method == "POST":
            form = newRFIDSensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.rfid.add(post)
                return redirect('/web/listRFID')
        else:
            form = newRFIDSensorForm(instance=post)
        return render(request, 'web/rfid_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def door_edit(request, puerta_id):
        post = get_object_or_404(puerta, pk=puerta_id)
        if request.method == "POST":
            form = newDOORSensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.puerta.add(post)
                return redirect('/web/listDOOR')
        else:
            form = newDOORSensorForm(instance=post)
        return render(request, 'web/door_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def led_edit(request, led_id):
        post = get_object_or_404(led, pk=led_id)
        if request.method == "POST":
            form = newLEDSensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.led.add(post)
                return redirect('/web/listLED')
        else:
            form = newLEDSensorForm(instance=post)
        return render(request, 'web/led_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def ldr_edit(request, ldr_id):
        post = get_object_or_404(ldr, pk=ldr_id)
        if request.method == "POST":
            form = newLDRSensorForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                request.user.userprofile.ldr.add(post)
                return redirect('/web/listLDR')
        else:
            form = newLDRSensorForm(instance=post)
        return render(request, 'web/ldr_edit.html', {'form': form})

@login_required(login_url = '/web/login')
def dht_delete(request, dht_id):
    post = get_object_or_404(dht, pk=dht_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listDHT')
    return render(request, 'web/dht_delete.html')

@login_required(login_url = '/web/login')
def mq2_delete(request, mq2_id):
    post = get_object_or_404(mq2, pk=mq2_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listMQ2')
    return render(request, 'web/mq2_delete.html')

@login_required(login_url = '/web/login')
def rfid_delete(request, rfid_id):
    post = get_object_or_404(rfid, pk=rfid_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listRFID')
    return render(request, 'web/rfid_delete.html')

@login_required(login_url = '/web/login')
def door_delete(request, door_id):
    post = get_object_or_404(puerta, pk=door_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listDOOR')
    return render(request, 'web/door_delete.html')

@login_required(login_url = '/web/login')
def ldr_delete(request, ldr_id):
    post = get_object_or_404(ldr, pk=ldr_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listLDR')
    return render(request, 'web/ldr_delete.html')

@login_required(login_url = '/web/login')
def led_delete(request, led_id):
    post = get_object_or_404(led, pk=led_id)
    if request.method == "POST":
        post.delete()
        return redirect('/web/listLED')
    return render(request, 'web/led_delete.html')
