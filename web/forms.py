from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led

class registroForm(UserCreationForm):
    class Meta:
        model = UserProfile
        field = ['username',
                'first_name',
                'last_name',
                'email',
                'uid',
                'codigoHogar',
                'password1',
                'password2',]
        labels = {'username': 'Nombre de usuario' ,
                    'first_name': 'Nombre',
                    'last_name': 'Apellido',
                    'email': 'Correo electronico',
                    'uid': 'Identificador UID',
                    'codigoHogar': 'Código del hogar',
                    'password1': 'Contraseña',
                    'password2':'Contraseña (confirmación)',}
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined' ,'password',
        'dht', 'rfid', 'mq2', 'ldr', 'puerta', 'led']

class newSensorForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ('nombre',
                'descripcion',
                'topic',
                'tipo',)

class editSensorForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ('nombre',
                'descripcion',
                'topic',)

class newDHTSensorForm(forms.ModelForm):
    class Meta:
        model = dht
        fields = ('nombre',
                'descripcion',
                'topic',)

class newRFIDSensorForm(forms.ModelForm):
    class Meta:
        model = rfid
        fields = ('nombre',
                'descripcion',
                'topic',)

class newMQ2SensorForm(forms.ModelForm):
    class Meta:
        model = mq2
        fields = ('nombre',
                'descripcion',
                'topic',)

class newLDRSensorForm(forms.ModelForm):
    class Meta:
        model = ldr
        fields = ('nombre',
                'descripcion',
                'topic',)

class newDOORSensorForm(forms.ModelForm):
    class Meta:
        model = puerta
        fields = ('nombre',
                'descripcion',
                'topic',)

class newLEDSensorForm(forms.ModelForm):
    class Meta:
        model = led
        fields = ('nombre',
                'descripcion',
                'topic',)

class editUserForm(UserChangeForm):
    class Meta:
        model = UserProfile
        field = ['first_name',
                    'last_name',
                    'email',
                    'uid',]
        labels = {'first_name': 'Nombre',
                        'last_name': 'Apellido',
                        'email': 'Correo electronico',
                        'uid': 'Identificador UID',}
        exclude = ['username', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined' , 'password1', 'password2', 'password',
            'dht', 'rfid', 'mq2', 'ldr', 'puerta', 'led', 'codigoHogar',]


class addSensorForm(forms.Form):
    nombre = forms.CharField(max_length= 250)
