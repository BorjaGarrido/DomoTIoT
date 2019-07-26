#Librerías, formularios y modelos usuados en las funciones del archivo views.py

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, newDHTSensorForm, newRFIDSensorForm, newDOORSensorForm, newMQ2SensorForm, newLDRSensorForm, newLEDSensorForm, editUserForm, addSensorForm, newSensorForm, editSensorForm
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

"""
    Nombre: modulo_list.
    Función: vista que solicita el html con los elementos divs a través de los cuales se puede
             acceder a los details de cada uno de los tipos de sensores.

             *Consultar modulo_list.html
"""
@login_required(login_url = '/web/login')
def modulo_list(request):

    return render(request, 'web/modulo_list.html')

"""
    Nombre: contacto.
    Función: vista que solicita el html con información de contacto sobre el desarrollador de la web.

             *Consultar contactos.html
"""
def contacto(request):

    return render(request, 'web/contacto.html')

"""
    Nombre: acerca.
    Función: vista que solicita el html con información acerca del desarrollador.

             *Consultar acerca.html
"""
def acerca(request):

    return render(request, 'web/acerca.html')

"""
    Nombre: inicio.
    Función: vista que muestra el html principal de la aplicación donde se encuentran los botones de
             login y registro.

             *Consultar inicio.html
"""
def inicio(request):

    return render(request, 'web/inicio.html')

"""
    Nombre: dhtDetail.
    Función: vista que muestra los valores de cada uno de los sensores de humedad y temperatura.

             *Consultar dhtDetail.html
"""
@login_required(login_url = '/web/login')
def dhtDetail(request):

    return render(request, 'web/dhtDetail.html')

"""
    Nombre: dhtDetail.
    Función: vista que muestra la información acerca de los sensores lectores RFID del sistema.

             *Consultar rfidDetail.html
"""
@login_required(login_url = '/web/login')
def rfidDetail(request):

    return render(request, 'web/rfidDetail.html')

"""
    Nombre: mq2Detail.
    Función: vista que muestra los valores de cada uno de los sensores que controlan la calidad del aire, es decir,
	     CO2, humo y gas LPG.

             *Consultar mq2Detail.html
"""
@login_required(login_url = '/web/login')
def mq2Detail(request):

    return render(request, 'web/mq2Detail.html')

"""
    Nombre: ldrDetail.
    Función: vista que muestra los valores de cada uno de los sensores LDR. Este sensor es capaz de medir la cantidad
	     de luz que hay en el ambiente.

             *Consultar ldrDetail.html
"""
@login_required(login_url = '/web/login')
def ldrDetail(request):

    return render(request, 'web/ldrDetail.html')

"""
    Nombre: doorDetail.
    Función: vista que muestra el estado de los sensores de las puertas, abierto o cerrado, y desde el cual se podrán
	     abrir al igual que se hace con el lector RFID.

             *Consultar doorDetail.html
"""
@login_required(login_url = '/web/login')
def doorDetail(request):

    return render(request, 'web/doorDetail.html')

"""
    Nombre: ledDetail.
    Función: vista que muestra el nivel de luz dado por los leds del hogar, desde este también se podrá controlar este
	     nivel. Todo ello controlado por los pines PWM del NodeMCU al que se conectan.

             *Consultar ledDetail.html
"""
@login_required(login_url = '/web/login')
def ledDetail(request):

    return render(request, 'web/ledDetail.html')


"""
    Nombre: registroUsuario.
    Función: vista usada para el registro de usuarios en el sistema. Esta función hace uso del formulario "registroForm"
	     existente en el archivo forms.py.

             *Consultar registroUsuario.html
"""
def registroUsuario(request):

    if request.method == 'POST': #Formulario vinculado a los datos POST
        form = registroForm(request.POST) #Llamada al formulario específico para el registro de un usuario

        if form.is_valid():
            form.save()
            return redirect(settings.LOGOUT_REDIRECT_URL) #Si el formulario es válido se guarda el usuario y se redirige a la página principal mediante el "REDIRECT"

    else:
        form = registroForm()

    return render(request, 'web/registro.html', {'form': form})


"""
    Nombre: userDetail.
    Función: vista usada para mostrar la información principal del usuario a modo de perfil del mismo, con
	     la idea de mostrar los cambios cuando de modifiquen sus datos.

             *Consultar userDetail.html
"""
@login_required(login_url = '/web/login')
def userDetail(request):
    #Recoge los datos actuales del usuario logueado y los guarda en las variables correspondientes
    member = request.user.userprofile
    nombre = member.first_name
    apellido = member.last_name
    username = member.username
    uid = member.uid
    codigoHogar = member.codigoHogar
    email = member.email
    #Devuelve las variables para que se puedan mostrar en el html
    return render(request, 'web/userDetail.html', {'nombre': nombre, 'apellido': apellido, 'username': username, 'uid': uid, 'codigoHogar': codigoHogar, 'email': email})

"""
    Nombre: editUser.
    Función: vista para modificar los datos del usuario a partir del formulario editUserForm del archivo forms.py.

             *Consultar editUser.html
"""
@login_required(login_url='/web/login/')
def editUser(request):

    if request.method == 'POST': #Formulario vinculado a los datos POST
        form = editUserForm(request.POST, instance=request.user.userprofile) #Formulario específico de modificación de datos

        if form.is_valid():
            form.save()
            return redirect('/web/userDetail') #Si el formulario es válido guarda los cambios y redirige a la vista del perfil del usuario

    else:
        form = editUserForm(instance=request.user.userprofile)

    return render(request, 'web/editUserForm.html', {'form': form})

"""
    Nombre: changePassword.
    Función: vista para cambiar la contraseña del usuario. Uso del formulario propio de Django, "PasswordChangeForm", que contempla
	     la contraseña inicial y la nueva contraseña con su correspondiente confirmación.

             *Consultar changePassword.html
"""
@login_required(login_url='/web/login/')
def changePassword(request):

    if request.method == 'POST': #Formulario vinculado a los datos POST
        form = PasswordChangeForm(data=request.POST, user=request.user) #Formulario de cambio de contraseña propio del framework Django.

        if form.is_valid(): #Si el formulario es válido guarda los cambios y redirige a la página principal, para volver a iniciar sesión
            form.save()
            return redirect('/')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'web/changePasswordForm.html', {'form': form})

"""
    Nombre: SignInView.
    Función: vista generérica para el inicio de sesión de un usuario. Uso de formulario propio de Django, "AuthenticationForm", el cual solo
	     contempla los campos Username y Password.

             *Consultar SignInView.html
"""
def SignInView(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid(): #Si el formulario es válido se recogen las variables introducidas y se comparan con la base de datos de los usuarios
            user = request.POST['username']
            passwd = request.POST['password']
            access = authenticate(username=user, password=passwd) #Búsqueda de usuario

            if access is not None: #Si el usuario existe
                if access.is_active:
                    login(request, access)
                    return redirect('/') #Se completa el logueo y se redirige a la página principal.
                else:
                    return render(request, 'web/inactive.html') #Si el usuario está inactivo, se muestra
            else:
                return render(request, 'web/nouser.html') #Si el usuario no existe se muestra
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request,'web/login.html', context)

"""
    Nombre: SignOutView.
    Función: vista generérica para el cierre de sesión del usuario logueado. Redirige a la página principal.
"""
@login_required(login_url='/web/login/')
def SignOutView(request):
    logout(request)
    return redirect('/')

@login_required(login_url = '/web/login')
def newSensor(request):

    if request.method == "POST":
        form = newSensorForm(request.POST)

        if form.is_valid():
            member = request.user.userprofile #Se recoge en una variable al usuario actual logueado que ha completado el formulario

            module= Modulo()
            module.nombre = form.cleaned_data['nombre']
            module.descripcion = form.cleaned_data['descripcion']
            module.topic = form.cleaned_data['topic']
            module.tipo = form.cleaned_data['tipo']
            module.codigoHogar = member.codigoHogar

            if module.tipo == "dht":
                dht_LOCAL = dht()
                dht_LOCAL.nombre = module.nombre
                dht_LOCAL.descripcion = module.descripcion
                dht_LOCAL.topic = module.topic
                dht_LOCAL.tipo = module.tipo
                dht_LOCAL.codigoHogar = module.codigoHogar
                dht_LOCAL.save()
                member.dht.add(dht_LOCAL)

            elif module.tipo == "rfid":
                rfid_LOCAL= rfid()
                rfid_LOCAL.nombre= module.nombre
                rfid_LOCAL.descripcion= module.descripcion
                rfid_LOCAL.topic= module.topic
                rfid_LOCAL.tipo= module.tipo
                rfid_LOCAL.codigoHogar = module.codigoHogar
                rfid_LOCAL.save()
                member.rfid.add(rfid_LOCAL)

            elif module.tipo == "mq2":
                mq2_LOCAL= mq2()
                mq2_LOCAL.nombre= module.nombre
                mq2_LOCAL.descripcion= module.descripcion
                mq2_LOCAL.topic= module.topic
                mq2_LOCAL.tipo= module.tipo
                mq2_LOCAL.codigoHogar = module.codigoHogar
                mq2_LOCAL.save()
                member.mq2.add(mq2_LOCAL)

            elif module.tipo == "ldr":
                ldr_LOCAL= ldr()
                ldr_LOCAL.nombre= module.nombre
                ldr_LOCAL.descripcion= module.descripcion
                ldr_LOCAL.topic= module.topic
                ldr_LOCAL.tipo= module.tipo
                ldr_LOCAL.codigoHogar = module.codigoHogar
                ldr_LOCAL.save()
                member.ldr.add(ldr_LOCAL)

            elif module.tipo == "led":
                led_LOCAL= led()
                led_LOCAL.nombre= module.nombre
                led_LOCAL.descripcion= module.descripcion
                led_LOCAL.topic= module.topic
                led_LOCAL.tipo= module.tipo
                led_LOCAL.codigoHogar = module.codigoHogar
                led_LOCAL.save()
                member.led.add(led_LOCAL)

            elif module.tipo == "puerta":
                puerta_LOCAL= puerta()
                puerta_LOCAL.nombre= module.nombre
                puerta_LOCAL.descripcion= module.descripcion
                puerta_LOCAL.topic= module.topic
                puerta_LOCAL.tipo= module.tipo
                puerta_LOCAL.codigoHogar = module.codigoHogar
                puerta_LOCAL.save()
                member.puerta.add(puerta_LOCAL)

            return redirect('/web/modulos') #Se guardan el formulario y la nueva instanciación del tipo de modelo DHT para el usuario
    else:
        form = newSensorForm()

    return render(request, 'web/newSensor.html', {'form': form})

@login_required(login_url = '/web/login')
def addSensor(request):

    if request.method == "POST":
        form = addSensorForm(request.POST) #Se rellena el formulario específico, el cual solo cotiene el nombre del sensor, que es único en todos los casos

        if form.is_valid():
            sensor = form.cleaned_data
            nombre = sensor.get('nombre') #Si el formulario es válido obtiene guarda el nombre en una variable
            member = request.user.userprofile #Si existe un sensor con ese nombre lo almacena en otra variable

            if dht.objects.filter(nombre=nombre).exists():
                sensor = dht.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.dht.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            elif mq2.objects.filter(nombre=nombre).exists():
                sensor = mq2.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.mq2.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            elif rfid.objects.filter(nombre=nombre).exists():
                sensor = rfid.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.rfid.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            elif ldr.objects.filter(nombre=nombre).exists():
                sensor = ldr.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.ldr.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            elif led.objects.filter(nombre=nombre).exists():
                sensor = led.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.led.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            elif puerta.objects.filter(nombre=nombre).exists():
                sensor = puerta.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar: #Si además ese sensor tiene el mismo códigoHogar que el usuario logueado lo añade a su lista de sensores
                    member.puerta.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')#Si el sensor es de otro hogar muestra mensaje de error
                    return redirect('/web/addSensor')

            else:
                messages.error(request, '*Sensor no encontrado') #Si no existe muestra mensaje de error
                return redirect('/web/addSensor')
    else:
        form = addSensorForm()

    return render(request, 'web/addSensor.html', {'form': form})


@login_required(login_url = '/web/login')
def Sensor_list(request):
    member = request.user.userprofile
    listaDHT = member.dht.all()
    listaMQ2 = member.mq2.all()
    listaRFID = member.rfid.all()
    listaLDR = member.ldr.all()
    listaLED = member.led.all()
    listaDOOR = member.puerta.all()
    return render(request, 'web/sensorList.html', {'listaDHT':listaDHT, 'listaMQ2':listaMQ2, 'listaRFID':listaRFID, 'listaLDR':listaLDR, 'listaLED':listaLED, 'listaDOOR':listaDOOR})

@login_required(login_url = '/web/login')
def edit_sensor(request, sensor_tipo, sensor_id):
    member = request.user.userprofile

    if sensor_tipo == "dht":
        post = member.dht.get(pk=sensor_id)

    elif sensor_tipo == "rfid":
        post = member.rfid.get(pk=sensor_id)

    elif sensor_tipo == "mq2":
        post = member.mq2.get(pk=sensor_id)

    elif sensor_tipo == "ldr":
        post = member.ldr.get(pk=sensor_id)

    elif sensor_tipo == "led":
        post = member.led.get(pk=sensor_id)

    elif sensor_tipo == "puerta":
        post = member.puerta.get(pk=sensor_id)

    if request.method == "POST":
        form = editSensorForm(request.POST, instance=post)
        if form.is_valid():
            post.nombre = form.cleaned_data['nombre']
            post.descripcion = form.cleaned_data['descripcion']
            post.topic = form.cleaned_data['topic']
            post.save()

        return redirect('/web/listSensor')

    else:
        form = editSensorForm(instance=post)

    return render(request, 'web/editSensor.html', {'form': form})

def delete_sensor(request, sensor_id, sensor_tipo):
    member = request.user.userprofile

    if request.method == "POST":
        if sensor_tipo == "dht":
            post = member.dht.get(pk=sensor_id)
            post.delete()
        elif sensor_tipo == "rfid":
            post = member.rfid.get(pk=sensor_id)
            post.delete()
        elif sensor_tipo == "mq2":
            post = member.mq2.get(pk=sensor_id)
            post.delete()
        elif sensor_tipo == "ldr":
            post = member.ldr.get(pk=sensor_id)
            post.delete()
        elif sensor_tipo == "led":
            post = member.led.get(pk=sensor_id)
            post.delete()
        elif sensor_tipo == "puerta":
            post = member.puerta.get(pk=sensor_id)
            post.delete()

        return redirect('/web/listSensor')

    return render(request, 'web/delete_sensor.html')
