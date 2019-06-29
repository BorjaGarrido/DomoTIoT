from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
	path('web/modulos/', views.modulo_list, name='modulo_list'),
	path('web/contacto/', views.contacto, name='contacto'),
	path('web/acerca/', views.acerca, name='acerca'),
    #path('web/login/', views.SignInView.as_view(), name='login'),
    path('web/login/', views.SignInView, name='login'),
    #path('web/registro/', views.registroUsuario.as_view(), name='registro'),
    path('web/registro/', views.registroUsuario, name='registro'),
    #path('web/logout/', views.SignOutView.as_view(), name='logout'),
    path('web/logout/', views.SignOutView, name='logout'),
    #path('web/newSensor/', views.newSensor.as_view(), name='nuevo_Sensor'),
    path('web/newSensor/', views.newSensor, name='nuevo_Sensor'),
]
