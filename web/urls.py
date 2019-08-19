from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [

    path('', views.inicio, name='inicio'),
    
	path('web/modulos/', views.modulo_list, name='modulo_list'),
	path('web/contacto/', views.contacto, name='contacto'),
	path('web/acerca/', views.acerca, name='acerca'),
    
    path('web/login/', views.SignInView, name='login'),
    path('web/registro/', views.registroUsuario, name='registro'),
    path('web/logout/', views.SignOutView, name='logout'),
    
    path('web/userDetail/', views.userDetail, name='userDetail'),
    path('web/editUserForm/', views.editUser, name='editUserForm'),
    path('web/changePasswordForm/', views.changePassword, name='changePasswordForm'),
    
    path('web/dhtDetail/', views.dhtDetail, name='dhtDetail'),
    path('web/rfidDetail/', views.rfidDetail, name='rfidDetail'),
    path('web/mq2Detail/', views.mq2Detail, name='dhtDetail'),
    path('web/ldrDetail/', views.ldrDetail, name='ldrDetail'),
    path('web/doorDetail/', views.doorDetail, name='doorDetail'),
    path('web/ledDetail/', views.ledDetail, name='ledDetail'),
    
    path('web/newSensor/', views.newSensor, name='nuevo_Sensor'),
    path('web/listSensor/', views.Sensor_list, name='Sensor_list,'),
    url(r'^web/(?P<sensor_tipo>\w+)/(?P<sensor_id>[0-9]+)/ed/$', views.edit_sensor, name='edit_sensor'),
    url(r'^web/(?P<sensor_tipo>\w+)/(?P<sensor_id>[0-9]+)/delete/$',views.delete_sensor, name='delete_sensor'),
    path('web/addSensor/', views.addSensor, name='add_Sensor'),
    
    url(r'^web/(?P<sensor_id>\d+)/open/$', views.open_door, name='open_door'),
    url(r'^web/(?P<sensor_id>\d+)/close/$', views.close_door, name='close_door'),
    
    url(r'^web/(?P<sensor_id>\d+)/ledoff/$', views.led_apagado, name='led_apagado'),
    url(r'^web/(?P<sensor_id>\d+)/ledlow/$', views.led_bajo, name='led_bajo'),
    url(r'^web/(?P<sensor_id>\d+)/ledmid/$', views.led_media, name='led_media'),
    url(r'^web/(?P<sensor_id>\d+)/ledmax/$', views.led_maxima, name='led_maxima'),
    url(r'^web/(?P<sensor_id>\d+)/ledauto/$', views.led_auto, name='led_auto'),
    url(r'^web/(?P<sensor_id>\d+)/ledprogram/$', views.led_datoProgramado, name='led_datoProgramado'),
    url(r'^web/(?P<sensor_id>\d+)/ledprogramOn/$', views.led_ProgramadoOn, name='led_ProgramadoOn'),
    url(r'^web/(?P<sensor_id>\d+)/ledprogramOff/$', views.led_ProgramadoOff, name='led_ProgramadoOff'),
    
    url(r'^web/(?P<sensor_id>\d+)/registroDht/$', views.registro_Datos_dht, name='registro_Datos_dht'),
    url(r'^web/(?P<sensor_id>\d+)/borrarRegistroDht/$', views.borrar_registro_dht, name='borrar_registro_dht'),    
    url(r'^web/(?P<sensor_id>\d+)/incidenciaDht/$', views.incidencia_Datos_dht, name='incidencia_Datos_dht'),
    url(r'^web/(?P<sensor_id>\d+)/borrarincidenciaDht/$', views.borrar_incidencia_dht, name='borrar_incidencia_dht'),
    
    url(r'^web/(?P<sensor_id>\d+)/registroMq2/$', views.registro_Datos_mq2, name='registro_Datos_mq2'),
    url(r'^web/(?P<sensor_id>\d+)/borrarRegistroMq2/$', views.borrar_registro_mq2, name='borrar_registro_mq2'),
    url(r'^web/(?P<sensor_id>\d+)/incidenciaMq2/$', views.incidencia_Datos_mq2, name='incidencia_Datos_mq2'),
    url(r'^web/(?P<sensor_id>\d+)/borrarincidenciaMq2/$', views.borrar_incidencia_mq2, name='borrar_incidencia_mq2'),
    
    url(r'^web/(?P<sensor_id>\d+)/registroRfid/$', views.registro_Datos_rfid, name='registro_Datos_rfid'),
    url(r'^web/(?P<sensor_id>\d+)/borrarRegistroRfid/$', views.borrar_registro_rfid, name='borrar_registro_rfid'),
]
