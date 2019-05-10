from django.urls import path
from . import views

urlpatterns = [
	path('', views.modulo_list, name='modulo_list'),
]