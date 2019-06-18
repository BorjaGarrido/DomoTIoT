from django.shortcuts import render
from django.utils import timezone
from .models import dht, rfid, mq2, ldr, led, puerta
from .forms import registroForm, newSensor
from .models import UserProfile, Modulo
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
import smtplib

# Create your views here.

def modulo_list(request):
    return render(request, 'web/modulo_list.html', {})

def contacto(request):
    return render(request, 'web/contacto.html')

def acerca(request):
    return render(request, 'web/acerca.html')

def inicio(request):
    return render(request, 'web/inicio.html')

"""class registroUsuario(CreateView):
    model = UserProfile
    template_name = "web/registro.html"
    form_class = registroForm
    success_url = "/"""

class SignInView(LoginView):
    template_name = 'web/login.html'

class SignOutView(LogoutView):
    pass

class newSensor(CreateView):
    model = Modulo
    template_name = "web/newSensor.html"
    form_class = newSensor
    success_url = "/web/modulos"

def registroUsuario(request):
    if request.method == 'POST':
        form = registroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        form = registroForm()
    return render(request, 'web/registro.html', {'form': form})
