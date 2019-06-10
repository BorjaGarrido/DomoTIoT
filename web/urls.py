from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
	path('web/modulos/', views.modulo_list, name='modulo_list'),
	path('web/contacto/', views.contacto, name='contacto'),
	path('web/acerca/', views.acerca, name='acerca'),
    path('web/login/', views.SignInView.as_view(), name='login'),
    path('web/registro/', views.registroUsuario.as_view(), name='registro'),
    path('web/logout/', views.SignOutView.as_view(), name='logout'),
]
