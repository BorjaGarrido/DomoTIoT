#Librerías, formularios y modelos usuados en las funciones del archivo views.py

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
from django.db.models import Q
from django.shortcuts import redirect
import datetime
import smtplib

"""
    Nombre: modulo_list.
    Función: vista que solicita el html con los elementos divs a
             través de los cuales se puede acceder a los details de cada uno
             de los tipos de sensores.

             *Consultar modulo_list.html
"""
@login_required(login_url = '/web/login')
def modulo_list(request):

    return render(request, 'web/modulo_list.html')

"""
    Nombre: contacto.
    Función: vista que solicita el html con información de contacto
             sobre el desarrollador de la web.

             *Consultar contactos.html
"""
def contacto(request):

    return render(request, 'web/contacto.html')

"""
    Nombre: acerca.
    Función: vista que solicita el html con información
             acerca del desarrollador.

             *Consultar acerca.html
"""
def acerca(request):

    return render(request, 'web/acerca.html')

"""
    Nombre: inicio.
    Función: vista que muestra el html principal de la aplicación donde
             se encuentran los botones de login y registro.

             *Consultar inicio.html
"""
def inicio(request):

    return render(request, 'web/inicio.html')

"""
    Nombre: dhtDetail.
    Función: vista que muestra los valores de cada uno de los
             sensores de humedad y temperatura.

             *Consultar dhtDetail.html
"""
@login_required(login_url = '/web/login')
def dhtDetail(request):

    return render(request, 'web/dhtDetail.html')

"""
    Nombre: dhtDetail.
    Función: vista que muestra la información acerca de los sensores
             lectores RFID del sistema.

             *Consultar rfidDetail.html
"""
@login_required(login_url = '/web/login')
def rfidDetail(request):

    return render(request, 'web/rfidDetail.html')

"""
    Nombre: mq2Detail.
    Función: vista que muestra los valores de cada uno de los sensores
             que controlan la calidad del aire, es decir, CO2, humo y gas LPG.

             *Consultar mq2Detail.html
"""
@login_required(login_url = '/web/login')
def mq2Detail(request):

    return render(request, 'web/mq2Detail.html')

"""
    Nombre: ldrDetail.
    Función: vista que muestra los valores de cada uno de los sensores LDR.
             Este sensor es capaz de medir la cantidad de luz que hay en
             el ambiente.

             *Consultar ldrDetail.html
"""
@login_required(login_url = '/web/login')
def ldrDetail(request):

    return render(request, 'web/ldrDetail.html')

"""
    Nombre: doorDetail.
    Función: vista que muestra el estado de los sensores de las puertas,
             abierto o cerrado, y desde el cual se podrán abrir al igual que
             se hace con el lector RFID.

             *Consultar doorDetail.html
"""
@login_required(login_url = '/web/login')
def doorDetail(request):

    return render(request, 'web/doorDetail.html')

"""
    Nombre: ledDetail.
    Función: vista que muestra el nivel de luz dado por los leds del hogar,
             desde este también se podrá controlar este nivel. Todo ello
             controlado por los pines PWM del NodeMCU al que se conectan.

             *Consultar ledDetail.html
"""
@login_required(login_url = '/web/login')
def ledDetail(request):

    return render(request, 'web/ledDetail.html')


"""
    Nombre: registroUsuario.
    Función: vista usada para el registro de usuarios en el sistema. Esta
             función hace uso del formulario "registroForm" existente en el
             archivo forms.py.

             *Consultar registroUsuario.html
"""
def registroUsuario(request):
    #Formulario vinculado a los datos POST
    if request.method == 'POST':
        #Llamada al formulario específico para el registro de un usuario
        form = registroForm(request.POST)

        if form.is_valid():
            form.save()
            #Si el formulario es válido se guarda el usuario y se redirige
            #   a la página principal mediante el "REDIRECT"
            return redirect(settings.LOGOUT_REDIRECT_URL)

    else:
        form = registroForm()

    return render(request, 'web/registro.html', {'form': form})


"""
    Nombre: userDetail.
    Función: vista usada para mostrar la información principal del usuario a
             modo de perfil del mismo, con la idea de mostrar los cambios
             cuando de modifiquen sus datos.

             *Consultar userDetail.html
"""
@login_required(login_url = '/web/login')
def userDetail(request):
    #Recoge los datos actuales del usuario logueado y los guarda
    #   en las variables correspondientes
    member = request.user.userprofile
    nombre = member.first_name
    apellido = member.last_name
    username = member.username
    uid = member.uid
    codigoHogar = member.codigoHogar
    email = member.email
    #Devuelve las variables para que se puedan mostrar en el html
    return render(request, 'web/userDetail.html', {'nombre': nombre,
        'apellido': apellido, 'username': username, 'uid': uid,
        'codigoHogar': codigoHogar, 'email': email})

"""
    Nombre: editUser.
    Función: vista para modificar los datos del usuario a partir del formulario
             editUserForm del archivo forms.py.

             *Consultar editUser.html
"""
@login_required(login_url='/web/login/')
def editUser(request):
    #Formulario vinculado a los datos POST
    if request.method == 'POST':
        #Formulario específico de modificación de datos
        form = editUserForm(request.POST, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('/web/userDetail') #Si el formulario es válido
            #   guarda los cambios y redirige a la vista del perfil del usuario

    else:
        form = editUserForm(instance=request.user.userprofile)

    return render(request, 'web/editUserForm.html', {'form': form})

"""
    Nombre: changePassword.
    Función: vista para cambiar la contraseña del usuario. Uso del formulario
             propio de Django, "PasswordChangeForm", que contempla la contrase-
             ña inicial y la nueva contraseña con su correspondiente confirma-
             ción.

             *Consultar changePassword.html
"""
@login_required(login_url='/web/login/')
def changePassword(request):
    #Formulario vinculado a los datos POST
    if request.method == 'POST':
        #Formulario de cambio de contraseña propio del framework Django.
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid(): #Si el formulario es válido guarda los cambios y
        #   redirige a la página principal, para volver a iniciar sesión
            form.save()
            return redirect('/')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'web/changePasswordForm.html', {'form': form})

"""
    Nombre: SignInView.
    Función: vista generérica para el inicio de sesión de un usuario. Uso de
             formulario propio de Django, "AuthenticationForm", el cual solo
	         contempla los campos Username y Password.

             *Consultar SignInView.html
"""
def SignInView(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid(): #Si el formulario es válido se recogen las
        #   variables introducidas y se comparan con la base de datos
        #   de los usuarios
            user = request.POST['username']
            passwd = request.POST['password']
            #Búsqueda de usuario
            access = authenticate(username=user, password=passwd)

            if access is not None: #Si el usuario existe
                if access.is_active:
                    login(request, access)
                    #Se completa el logueo y se redirige a la página principal
                    return redirect('/')
                else:
                    #Si el usuario está inactivo, se muestra
                    return render(request, 'web/inactive.html')
            else:
                #Si el usuario no existe se muestra
                return render(request, 'web/nouser.html')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request,'web/login.html', context)

"""
    Nombre: SignOutView.
    Función: vista generérica para el cierre de sesión del usuario logueado.
             Redirige a la página principal.
"""
@login_required(login_url='/web/login/')
def SignOutView(request):
    logout(request)
    return redirect('/')

"""
    Nombre: newSensor.
    Función: vista usada para el registro de un nuevo sensor. Se hace uso
             del formulario específico newSensorForm que permite definir el
             nombre, descripcion, topic y tipo de cada sensor.

             *Consultar newSensor.html
"""
@login_required(login_url = '/web/login')
def newSensor(request):

    if request.method == "POST":
        #Se recogen los datos del sensor y se almacenan en la variable
        form = newSensorForm(request.POST)

        if form.is_valid():
            member = request.user.userprofile #Se recoge en una variable al
            #   usuario actual logueado que ha completado el formulario

            module= Modulo() #Se crea una instanciación del modelo Modulo()
            #   y se rellana con los datos obtenidos del formulario
            module.nombre = form.cleaned_data['nombre']
            module.descripcion = form.cleaned_data['descripcion']
            module.topic = form.cleaned_data['topic']
            module.tipo = form.cleaned_data['tipo']
            #Se introduce el codigoHogar propio del usuario logueado
            module.codigoHogar = member.codigoHogar

            #Se compara el tipo del sensor introducido y se
            # rellenan las variables
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
            #Se guardan el formulario y la nueva instanciación del
            #   tipo de sensor para el usuario
            return redirect('/web/modulos')
    else:
        form = newSensorForm()

    return render(request, 'web/newSensor.html', {'form': form})

"""
    Nombre: addSensor.
    Función: vista usada para añadir un sensor ya existente en un hogar pero
             registrado por otro usuario. Se usa el formulario específico
             addSensorForm y la variable codigoHogar.

             *Consultar addSensor.html
"""
@login_required(login_url = '/web/login')
def addSensor(request):

    if request.method == "POST":
        form = addSensorForm(request.POST) #Se rellena el formulario
        #   específico, el cual solo cotiene el nombre del sensor que es
        #   único en todos los casos

        if form.is_valid():
            sensor = form.cleaned_data
            #Si el formulario es válido se guarda el nombre en una variable
            nombre = sensor.get('nombre')
            member = request.user.userprofile

            if dht.objects.filter(nombre=nombre).exists():
                sensor = dht.objects.get(nombre=nombre) #Si existe un sensor
                #   dht con ese nombre lo almacena en otra variable

                if sensor.codigoHogar == member.codigoHogar: #Si además ese
                #sensor tiene el mismo códigoHogar que el usuario logueado
                #   lo añade a su lista de sensores
                    member.dht.add(sensor)
                    #Redirecciona a la lista de modulos
                    return redirect('/web/modulos')
                else:
                    #Si el sensor es de otro hogar muestra mensaje de error
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    #Se redirige de vuelta al addSensor
                    return redirect('/web/addSensor')

            elif mq2.objects.filter(nombre=nombre).exists():
                sensor = mq2.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar:
                    member.mq2.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    return redirect('/web/addSensor')

            elif rfid.objects.filter(nombre=nombre).exists():
                sensor = rfid.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar:
                    member.rfid.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    return redirect('/web/addSensor')

            elif ldr.objects.filter(nombre=nombre).exists():
                sensor = ldr.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar:
                    member.ldr.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    return redirect('/web/addSensor')

            elif led.objects.filter(nombre=nombre).exists():
                sensor = led.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar:
                    member.led.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    return redirect('/web/addSensor')

            elif puerta.objects.filter(nombre=nombre).exists():
                sensor = puerta.objects.get(nombre=nombre)

                if sensor.codigoHogar == member.codigoHogar:
                    member.puerta.add(sensor)
                    return redirect('/web/modulos')
                else:
                    messages.error(request, '*Sensor no perteneciente al hogar')
                    return redirect('/web/addSensor')

            else:
                #Si no existe muestra mensaje de error
                messages.error(request, '*Sensor no encontrado')
                return redirect('/web/addSensor')
    else:
        form = addSensorForm()

    return render(request, 'web/addSensor.html', {'form': form})

"""
    Nombre: Sensor_list.
    Función: vista que únicamente muestra la lista de sensores
             disponibles de un usuario.

             *Consultar sensorList.html
"""
@login_required(login_url = '/web/login')
def Sensor_list(request):
    # Almacena en una variable los datos del usuario logueado
    member = request.user.userprofile
    # Obtiene en listas todos los sensores de cada tipo del usuario logueado
    listaDHT = member.dht.all()
    listaMQ2 = member.mq2.all()
    listaRFID = member.rfid.all()
    listaLDR = member.ldr.all()
    listaLED = member.led.all()
    listaDOOR = member.puerta.all()
    return render(request, 'web/sensorList.html', {'listaDHT':listaDHT,
            'listaMQ2':listaMQ2, 'listaRFID':listaRFID, 'listaLDR':listaLDR,
            'listaLED':listaLED, 'listaDOOR':listaDOOR})

"""
    Nombre: Sensor_list.
    Función: esta vista permite modificar el nombre, descripcion y topic
             de cada sensor registrado por el usuario. Se precisa de otro
             formulario, editSensorForm, que no pida el tipo, pues este
             no se puede moficar.

             *Consultar editSensor.html
"""
@login_required(login_url = '/web/login')
def edit_sensor(request, sensor_tipo, sensor_id):
    # Se almacenan los datos del usuario logueado
    member = request.user.userprofile

    # Se comprueba el tipo de sensor que es y se almacena
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
        # Si el formulario es válido se modifican los campos del sensor
        #   en concreto.
        if form.is_valid():
            post.nombre = form.cleaned_data['nombre']
            post.descripcion = form.cleaned_data['descripcion']
            post.topic = form.cleaned_data['topic']
            post.save()

        return redirect('/web/listSensor')

    else:
        form = editSensorForm(instance=post)
    #Se redirecciona al template en específico
    return render(request, 'web/editSensor.html', {'form': form})

"""
    Nombre: Sensor_list.
    Función: esta vista permite elimar un sensor en concreto. Sigue una
             estructura similar al editSensor en cuanto a la búsqueda del
             sensor.

             *Consultar editSensor.html
"""
def delete_sensor(request, sensor_id, sensor_tipo):
    # Se almacenan los datos del usuario logueado
    member = request.user.userprofile

    #Se confirma que se quiere eliminar el sensor tras realizar su búsqueda
    #   mediante la clave primaria
    if request.method == "POST":
        if sensor_tipo == "dht":
            post = member.dht.get(pk=sensor_id)
            post.delete() # delete() eliminar de la BBDD al sensor con esa pk
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
