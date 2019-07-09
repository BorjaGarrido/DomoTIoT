from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led

class registroForm(UserCreationForm):
    class Meta:
        model = UserProfile
        field = ['username',
                'first_name',
                'last_name',
                'email',
                'uid',]
        labels = {'username': 'Nombre de usuario' ,
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'email': 'Correo electronico',
                    'uid': 'Identificador UID',}
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined' ,'password',
        'dht', 'rfid', 'mq2', 'ldr', 'puerta', 'led']

class newDHTSensorForm(forms.ModelForm):
    class Meta:
        model = dht
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['temperatura', 'humedad']

class newRFIDSensorForm(forms.ModelForm):
    class Meta:
        model = rfid
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['uid']

class newMQ2SensorForm(forms.ModelForm):
    class Meta:
        model = mq2
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['lpg', 'co2', 'smoke']

class newLDRSensorForm(forms.ModelForm):
    class Meta:
        model = ldr
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['luminosidad']

class newDOORSensorForm(forms.ModelForm):
    class Meta:
        model = puerta
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['estado']

class newLEDSensorForm(forms.ModelForm):
    class Meta:
        model = led
        field = ['nombre',
                'descripcion',
                'topic',]
        labels = {'nombre': 'Nombre' ,
                    'descripcion': 'Descripción',
                    'topic': 'Topic',}
        exclude = ['nivel']
