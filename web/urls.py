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
    #url(r'^web/(?P<sensor_id>[0-9]+)/dht/mqtt/$',views.dht_mqtt, name='dht_mqtt'),
]
