from django.urls import path
from . import views


urlpatterns = [
    path('', views.misNotificaciones, name='notificaciones'),
    path('eliminar/<int:pk>', views.eliminarNoti, name='eliminarNotificacion')
]