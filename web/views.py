from django.shortcuts import render
from django.utils import timezone
from .models import dht, rfid, mq2, ldr, led, puerta
from .forms import registroForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse



# Create your views here.

def modulo_list(request):
    return render(request, 'web/modulo_list.html', {})

def contacto(request):
    return render(request, 'web/contacto.html')

def acerca(request):
    return render(request, 'web/acerca.html')

def inicio(request):
    return render(request, 'web/inicio.html')

class registroUsuario(CreateView):
    model = User
    template_name = "web/registro.html"
    form_class = registroForm
    success_url = "/"
