from django.shortcuts import render, render_to_response
from django.utils import timezone
from datetime import datetime
from django.utils import formats
from .models import dht, rfid, mq2, ldr, led, puerta
from .forms import registroForm, newSensorForm
from .models import UserProfile, Modulo
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
import datetime
import smtplib

# Create your views here.
@login_required(login_url = '/web/login')
def modulo_list(request):
    dia = datetime.datetime.now().strftime('%d/%m/%Y')
    hora = datetime.datetime.now().strftime('%H:%M:%S')
    return render(request, 'web/modulo_list.html', {'dia': dia ,'hora': hora})

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

"""class SignInView(LoginView):
    template_name = 'web/login.html'"""

"""@login_required(login_url = '/users/login')
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/')
        else:
            form = PostForm()
        return render(request, 'polls/post_edit.html', {'form': form})"""

@login_required(login_url = '/web/login')
def newSensor(request):
    if request.method == "POST":
        form = newSensorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            """post.author = request.user
            post.published_date = timezone.now()"""
            post.save()
            return redirect('/web/modulos')
    else:
        form = newSensorForm()
    return render(request, 'web/newSensor.html', {'form': form})

"""class newSensor(CreateView):
    model = Modulo
    template_name = "web/newSensor.html"
    form_class = newSensor
    success_url = "/web/modulos"""

def registroUsuario(request):
    if request.method == 'POST':
        form = registroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        form = registroForm()
    return render(request, 'web/registro.html', {'form': form})


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
