from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciarSesion, name='login'),
    path('logout/', views.cerrarSesion, name='cerrarSesion'),
    path('perfil/', views.editarUsuario, name='perfil')
]