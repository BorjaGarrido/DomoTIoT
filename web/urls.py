from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
	path('web/modulos/', views.modulo_list, name='modulo_list'),
	path('web/contacto/', views.contacto, name='contacto'),
	path('web/acerca/', views.acerca, name='acerca'),
    path('web/dhtDetail/', views.dhtDetail, name='dhtDetail'),
    path('web/rfidDetail/', views.rfidDetail, name='rfidDetail'),
    path('web/mq2Detail/', views.mq2Detail, name='dhtDetail'),
    path('web/ldrDetail/', views.ldrDetail, name='ldrDetail'),
    path('web/doorDetail/', views.doorDetail, name='doorDetail'),
    path('web/ledDetail/', views.ledDetail, name='ledDetail'),
    #path('web/login/', views.SignInView.as_view(), name='login'),
    path('web/login/', views.SignInView, name='login'),
    #path('web/registro/', views.registroUsuario.as_view(), name='registro'),
    path('web/registro/', views.registroUsuario, name='registro'),
    #path('web/logout/', views.SignOutView.as_view(), name='logout'),
    path('web/logout/', views.SignOutView, name='logout'),
    #path('web/newSensor/', views.newSensor.as_view(), name='nuevo_Sensor'),
    path('web/newDhtSensor/', views.newDHTSensor, name='nuevo_DHTSensor'),
    path('web/newRfidSensor/', views.newRFIDSensor, name='nuevo_RFIDSensor'),
    path('web/newMq2Sensor/', views.newMQ2Sensor, name='nuevo_MQ2Sensor'),
    path('web/newLdrSensor/', views.newLDRSensor, name='nuevo_LDRSensor'),
    path('web/newDoorSensor/', views.newDOORSensor, name='nuevo_DOORSensor'),
    path('web/newLedSensor/', views.newLEDSensor, name='nuevo_LEDSensor'),
]
