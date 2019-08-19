##################################IMPORTS####################################
"""
Librerías, funciones y modelos importados para el desarrollo de la aplicación
web
"""
#############################################################################

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .forms import registroForm, editUserForm
from .forms import  addSensorForm, newSensorForm, editSensorForm
from .forms import  editLedHourForm
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
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template import RequestContext

##################################FUNCIONES####################################
"""
Funciones propias implementadas en el desarrollo de la aplicación web
"""
##############################################################################

"""
    Nombre: modulo_list.
    Función: vista que solicita el html con los elementos divs a
             través de los cuales se puede acceder a los details de cada uno
             de los tipos de sensores.

             *Consultar modulo_list.html
"""
@login_required(login_url = '/web/login')
def modulo_list(request):
    member = request.user.userprofile

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
    
    member = request.user.userprofile
    listaDHT = member.dht.all()
    
    #dhtData.delay()
        
    return render(request, 'web/dhtDetail.html', {'listaDHT':listaDHT})

"""
    Nombre: dhtDetail.
    Función: vista que muestra la información acerca de los sensores
             lectores RFID del sistema.

             *Consultar rfidDetail.html
"""

@login_required(login_url = '/web/login')
def rfidDetail(request):
    
    member = request.user.userprofile
    listaRFID = member.rfid.all()

    return render(request, 'web/rfidDetail.html', {'listaRFID': listaRFID })

"""
    Nombre: mq2Detail.
    Función: vista que muestra los valores de cada uno de los sensores
             que controlan la calidad del aire, es decir, CO2, humo y gas LPG.

             *Consultar mq2Detail.html
"""
@login_required(login_url = '/web/login')
def mq2Detail(request):
    
    member = request.user.userprofile
    listaMQ2 = member.mq2.all()

    return render(request, 'web/mq2Detail.html', {'listaMQ2':listaMQ2})

"""
    Nombre: ldrDetail.
    Función: vista que muestra los valores de cada uno de los sensores LDR.
             Este sensor es capaz de medir la cantidad de luz que hay en
             el ambiente.

             *Consultar ldrDetail.html
"""
@login_required(login_url = '/web/login')
def ldrDetail(request):
    
    member = request.user.userprofile
    listaLDR = member.ldr.all()

    return render(request, 'web/ldrDetail.html', {'listaLDR': listaLDR})

"""
    Nombre: doorDetail.
    Función: vista que muestra el estado de los sensores de las puertas,
             abierto o cerrado, y desde el cual se podrán abrir al igual que
             se hace con el lector RFID.

             *Consultar doorDetail.html
"""
@login_required(login_url = '/web/login')
def doorDetail(request):
    
    member = request.user.userprofile
    listaPuerta = member.puerta.all()

    return render(request, 'web/doorDetail.html', {'listaPuerta': listaPuerta})

"""
    Nombre: ledDetail.
    Función: vista que muestra el nivel de luz dado por los leds del hogar,
             desde este también se podrá controlar este nivel. Todo ello
             controlado por los pines PWM del NodeMCU al que se conectan.

             *Consultar ledDetail.html
"""
@login_required(login_url = '/web/login')
def ledDetail(request):
    
    member = request.user.userprofile
    listaLed = member.led.all()

    return render(request, 'web/ledDetail.html', {'listaLed': listaLed})


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
            #Si el formulario es válido se guarda el usuario, se le manda
            # un mensaje y se redirige a la pagina principal.
            
            emailTo = request.POST.get('email')
            
            username = request.POST.get('username')
            
            nombre = request.POST.get('first_name')   
            
            apellido = request.POST.get('last_name') 
            
            uid = request.POST.get('uid') 
            
            codigoHogar = request.POST.get('codigoHogar') 
            
            ipBroker = request.POST.get('ipBroker') 
            
            #render_to_string permite renderizar un html en un string
            body = render_to_string('web/email_registroOK.html',
                {'username': username,
                 'nombre': nombre,
                 'apellido': apellido,
                 'uid': uid,
                 'codigoHogar': codigoHogar,
                 'ipBroker': ipBroker,
                })
            
            #Se envía el email con el string renderizado anteriormente
            email_message = EmailMessage(
                subject='Bienvenido',
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=[emailTo],
            )
            
            email_message.content_subtype = 'html'
            email_message.send()
            
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
    ipBroker = member.ipBroker
    email = member.email
    #Devuelve las variables para que se puedan mostrar en el html
    return render(request, 'web/userDetail.html', {'nombre': nombre,
        'apellido': apellido, 'username': username, 'uid': uid,
        'codigoHogar': codigoHogar, 'email': email, 'ipBroker': ipBroker})

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
                    
                    member = request.user.userprofile
                    
                    member.conectado = True
                    member.save()
                    
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
    
    member = request.user.userprofile
    
    member.conectado = False
    member.save()
    
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
            module.habitacion = form.cleaned_data['habitacion']
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
                dht_LOCAL.habitacion = module.habitacion
                dht_LOCAL.topic = module.topic
                dht_LOCAL.tipo = module.tipo
                dht_LOCAL.codigoHogar = module.codigoHogar
                dht_LOCAL.save()
                member.dht.add(dht_LOCAL)

            elif module.tipo == "rfid":
                rfid_LOCAL= rfid()
                rfid_LOCAL.nombre= module.nombre
                rfid_LOCAL.descripcion= module.descripcion
                rfid_LOCAL.habitacion = module.habitacion
                rfid_LOCAL.topic= module.topic
                rfid_LOCAL.tipo= module.tipo
                rfid_LOCAL.codigoHogar = module.codigoHogar
                rfid_LOCAL.save()
                member.rfid.add(rfid_LOCAL)

            elif module.tipo == "mq2":
                mq2_LOCAL= mq2()
                mq2_LOCAL.nombre= module.nombre
                mq2_LOCAL.descripcion= module.descripcion
                mq2_LOCAL.habitacion = module.habitacion
                mq2_LOCAL.topic= module.topic
                mq2_LOCAL.tipo= module.tipo
                mq2_LOCAL.codigoHogar = module.codigoHogar
                mq2_LOCAL.save()
                member.mq2.add(mq2_LOCAL)

            elif module.tipo == "ldr":
                ldr_LOCAL= ldr()
                ldr_LOCAL.nombre= module.nombre
                ldr_LOCAL.descripcion= module.descripcion
                ldr_LOCAL.habitacion = module.habitacion
                ldr_LOCAL.topic= module.topic
                ldr_LOCAL.tipo= module.tipo
                ldr_LOCAL.codigoHogar = module.codigoHogar
                ldr_LOCAL.save()
                member.ldr.add(ldr_LOCAL)

            elif module.tipo == "led":
                led_LOCAL= led()
                led_LOCAL.nombre= module.nombre
                led_LOCAL.descripcion= module.descripcion
                led_LOCAL.habitacion = module.habitacion
                led_LOCAL.topic= module.topic
                led_LOCAL.tipo= module.tipo
                led_LOCAL.codigoHogar = module.codigoHogar
                led_LOCAL.save()
                member.led.add(led_LOCAL)

            elif module.tipo == "puerta":
                puerta_LOCAL= puerta()
                puerta_LOCAL.nombre= module.nombre
                puerta_LOCAL.descripcion= module.descripcion
                puerta_LOCAL.habitacion = module.habitacion
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
    Nombre: edit_sensor.
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
    Nombre: delete_sensor.
    Función: esta vista permite elimar un sensor en concreto. Sigue una
             estructura similar al editSensor en cuanto a la búsqueda del
             sensor.

             *Consultar editSensor.html
"""
@login_required(login_url = '/web/login')
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


"""
    Nombre: open_door.
    Función: vista que realiza una conexión al broker del sistema y 
             permite abrir una puerta cerrada del hogar.

"""
@login_required(login_url = '/web/login')
def open_door(request, sensor_id):
    
    member = request.user.userprofile
    
    door = member.puerta.get(pk=sensor_id)
    
    if door.estado == False:
        publish.single(door.topic, 1, hostname = member.ipBroker)
        
        door.estado = True
        
        door.save()
        member.puerta.add(door)
    
    return redirect('/web/doorDetail')
    
"""
    Nombre: close_door.
    Función: vista que realiza una conexión al broker del sistema y 
             permite cerrar una puerta abierta del hogar.

"""
@login_required(login_url = '/web/login')
def close_door(request, sensor_id):
    
    member = request.user.userprofile
    
    door = member.puerta.get(pk=sensor_id)
    
    if door.estado == True:
        publish.single(door.topic, 0, hostname = member.ipBroker)
        
        door.estado = False
        
        door.save()
        member.puerta.add(door)
    
    return redirect('/web/doorDetail')

"""
    Nombre: led_apagado.
    Función: vista que realiza una conexión al broker del sistema y 
             permite apagar los leds de una habitación.

"""
@login_required(login_url = '/web/login')
def led_apagado(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.auto == True:
        
        led.auto = False
        
        led.save()
        member.led.add(led)
    
    publish.single(led.topic, 0, hostname = member.ipBroker)
    
    led.nivel = 0
    led.save()
    member.led.add(led)
    
    return redirect('/web/ledDetail')
    
"""
    Nombre: led_bajo.
    Función: vista que realiza una conexión al broker del sistema y 
             permite cambiar la intensidad de un led a baja de una
             habitación.

"""
@login_required(login_url = '/web/login')
def led_bajo(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.auto == True:
        
        led.auto = False
        
        led.save()
        member.led.add(led)
    
    publish.single(led.topic, 124, hostname = member.ipBroker)
    
    led.nivel = 124
    led.save()
    member.led.add(led)
    
    return redirect('/web/ledDetail')
    
"""
    Nombre: led_medio.
    Función: vista que realiza una conexión al broker del sistema y 
             permite cambiar la intensidad de un led a media de una
             habitación.

"""
@login_required(login_url = '/web/login')
def led_media(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.auto == True:
        
        led.auto = False
        
        led.save()
        member.led.add(led)
    
    publish.single(led.topic, 512, hostname = member.ipBroker)
    
    led.nivel = 512
    led.save()
    member.led.add(led)
    
    return redirect('/web/ledDetail')

"""
    Nombre: led_maxima.
    Función: vista que realiza una conexión al broker del sistema y 
             permite cambiar la intensidad de un led a máxima de una
             habitación.

"""
@login_required(login_url = '/web/login')
def led_maxima(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.auto == True:
        
        led.auto = False
        
        led.save()
        member.led.add(led)
    
    publish.single(led.topic, 1024, hostname = member.ipBroker)
    
    led.nivel = 1024    
    led.save()
    member.led.add(led)
    
    return redirect('/web/ledDetail')


"""
    Nombre: led_auto.
    Función: vista que realiza una conexión al broker del sistema y 
             permite cambiar a automático la intensidad del led de una
             habitación.

"""
@login_required(login_url = '/web/login')
def led_auto(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.auto == False:
        
        led.auto = True
        
        led.save()
        member.led.add(led)
    
    
    return redirect('/web/ledDetail')
    
"""
    Nombre: programarLed.
    Función: vista que permite programar la hora de encendido y apagado 
             del led, así como activar si se quiere mantener la progra-
             mación o no.
"""
@login_required(login_url = '/web/login')
def led_datoProgramado(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if request.method == "POST":
        form = editLedHourForm(request.POST, instance=led)
        # Si el formulario es válido se modifican las horas del led
        #   en concreto.
        if form.is_valid():
            led.horaInicio = form.cleaned_data['horaInicio']
            led.horaFin = form.cleaned_data['horaFin']
            led.nivelProgramado = form.cleaned_data['nivelProgramado']
            led.autoProgramado = True
            led.save()

        return redirect('/web/ledDetail')

    else:
        form = editLedHourForm(instance=led)
    #Se redirecciona al template en específico
    return render(request, 'web/led_program.html', {'form': form})

"""
    Nombre: led_ProgramadoOn.
    Función: vista que activa el temporizador del encendido
              o apagado de un led específico.

"""
@login_required(login_url = '/web/login')
def led_ProgramadoOn(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.autoProgramado == False:
        
        led.autoProgramado = True
        
        led.save()
        member.led.add(led)
    
    
    return redirect('/web/ledDetail')
    
"""
    Nombre: led_ProgramadoOff.
    Función: vista que desactiva el temporizador del encendido
              o apagado de un led específico.

"""
@login_required(login_url = '/web/login')
def led_ProgramadoOff(request, sensor_id):
    
    member = request.user.userprofile
    
    led = member.led.get(pk=sensor_id)
    
    if led.autoProgramado == True:
        
        led.autoProgramado = False
        
        led.save()
        member.led.add(led)
    
    
    return redirect('/web/ledDetail')

"""
    Nombre: registro_Datos_dht.
    Función: vista que recoge los datos diarios de los sensores DHT
             y los muestra.

"""
@login_required(login_url = '/web/login')
def registro_Datos_dht(request, sensor_id):
    
    member = request.user.userprofile
    
    dht = member.dht.get(pk=sensor_id)
    registros = registroDHT.objects.filter(dht=dht)
    
    return render(request, 'web/registroDht.html', {'registros': registros, 'dht': dht})

"""
    Nombre: borrar_registro_dht.
    Función: vista que permite eleminar todos los registros de un 
             sensor dht.

"""
@login_required(login_url = '/web/login')
def borrar_registro_dht(request, sensor_id):
    
    member = request.user.userprofile
    dht = member.dht.get(pk=sensor_id)
    
    if request.method == "POST":
        registroDHT.objects.filter(dht=dht).delete()

        return redirect('/web/%s/registroDht/' %sensor_id)
        
    return render(request, 'web/delete_registro_dht.html', {'dht': dht})


"""
    Nombre: incidencia_Datos_dht.
    Función: vista que recoge las incidencias de los sensores DHT
             y las muestra.

"""
@login_required(login_url = '/web/login')
def incidencia_Datos_dht(request, sensor_id):
    
    member = request.user.userprofile
    
    dht = member.dht.get(pk=sensor_id)
    incidencias = incidenciaDHT.objects.filter(dht=dht)
    
    return render(request, 'web/incidenciaDHT.html', {'incidencias': incidencias, 'dht': dht})

"""
    Nombre: borrar_incidencia_dht.
    Función: vista que permite eliminar todas las incidencias de un 
             sensor dht.
"""
@login_required(login_url = '/web/login')
def borrar_incidencia_dht(request, sensor_id):
    
    member = request.user.userprofile
    dht = member.dht.get(pk=sensor_id)
    
    if request.method == "POST":
        incidenciaDHT.objects.filter(dht=dht).delete()

        return redirect('/web/%s/incidenciaDht/' %sensor_id)
        
    return render(request, 'web/delete_incidencia_dht.html', {'dht': dht})


"""
    Nombre: registro_Datos_mq2.
    Función: vista que recoge los datos diarios de los sensores MQ2
             y los muestra.

"""
@login_required(login_url = '/web/login')
def registro_Datos_mq2(request, sensor_id):
    
    member = request.user.userprofile
    
    mq2 = member.mq2.get(pk=sensor_id)
    registros = registroMQ2.objects.filter(mq2=mq2)
    
    return render(request, 'web/registroMq2.html', {'registros': registros, 'mq2': mq2})

"""
    Nombre: borrar_registro_mq2.
    Función: vista que permite eleminar todos los registros de un 
             sensor mq2.

"""
@login_required(login_url = '/web/login')
def borrar_registro_mq2(request, sensor_id):
    
    member = request.user.userprofile
    mq2 = member.mq2.get(pk=sensor_id)
    
    if request.method == "POST":
        registroMQ2.objects.filter(mq2=mq2).delete()

        return redirect('/web/%s/registroMq2/' %sensor_id)
        
    return render(request, 'web/delete_registro_mq2.html', {'mq2': mq2})


"""
    Nombre: incidencia_Datos_mq2.
    Función: vista que recoge las incidencias de los sensores MQ2
             y las muestra.

"""
@login_required(login_url = '/web/login')
def incidencia_Datos_mq2(request, sensor_id):
    
    member = request.user.userprofile
    
    mq2 = member.mq2.get(pk=sensor_id)
    incidencias = incidenciaMQ2.objects.filter(mq2=mq2)
    
    return render(request, 'web/incidenciaMq2.html', {'incidencias': incidencias, 'mq2': mq2})

"""
    Nombre: borrar_incidencia_mq2.
    Función: vista que permite eliminar todas las incidencias de un 
             sensor mq2.
"""
@login_required(login_url = '/web/login')
def borrar_incidencia_mq2(request, sensor_id):
    
    member = request.user.userprofile
    mq2 = member.mq2.get(pk=sensor_id)
    
    if request.method == "POST":
        incidenciaMQ2.objects.filter(mq2=mq2).delete()

        return redirect('/web/%s/incidenciaMq2/' %sensor_id)
        
    return render(request, 'web/delete_incidencia_mq2.html', {'mq2': mq2})

"""
    Nombre: registro_Datos_rfid.
    Función: vista que recoge la hora y fecha en la que se usa una 
             tarjeta RFID en un lector RFID del usuario.

"""
@login_required(login_url = '/web/login')
def registro_Datos_rfid(request, sensor_id):
    
    member = request.user.userprofile
    
    rfid = member.rfid.get(pk=sensor_id)
    registros = registroRFID.objects.filter(rfid=rfid)
    
    return render(request, 'web/registroRfid.html', {'registros': registros, 'rfid': rfid})

"""
    Nombre: borrar_registro_rfid.
    Función: vista que permite eleminar todos los registros de un 
             sensor rfid.

"""
@login_required(login_url = '/web/login')
def borrar_registro_rfid(request, sensor_id):
    
    member = request.user.userprofile
    rfid = member.rfid.get(pk=sensor_id)
    
    if request.method == "POST":
        registroRFID.objects.filter(rfid=rfid).delete()

        return redirect('/web/%s/registroRfid/' %sensor_id)
        
    return render(request, 'web/delete_registro_rfid.html', {'rfid': rfid})
