from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile, Modulo

class registroForm(UserCreationForm):
    class Meta:
        model = UserProfile
        field = ['username',
                'first_name',
                'last_name',
                'email',
                'uid',]
        labels = {'username': 'Nickname' ,
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'email': 'Correo electronico',
                    'uid': 'Identificador UID',}
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined' ,'password',
        'dht', 'rfid', 'mq2', 'ldr', 'puerta', 'led']

class newSensor(forms.ModelForm):
    class Meta:
        model = Modulo
        field = ['nombre',
                'numero',
                'descripcion',
                'topic',
                'tipo',]
        labels = {'nombre': 'Nombre' ,
                    'numero': 'Número identificador',
                    'descripcion': 'Descripción',
                    'topic': 'Topic',
                    'tipo': 'Tipo',}
        exclude = []
