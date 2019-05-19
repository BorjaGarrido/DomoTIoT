from django.shortcuts import render
from django.utils import timezone
from .models import dht, rfid, mq2, ldr, led, puerta

# Create your views here.

def modulo_list(request):
    return render(request, 'web/modulo_list.html', {})

def contacto(request):
    return render(request, 'web/contacto.html')

def acerca(request):
    return render(request, 'web/acerca.html')
