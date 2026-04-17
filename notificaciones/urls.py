from django.urls import path
from . import views

urlpatterns = [
    path("", views.notificacion_lista, name="notificacion_lista"),
    path("<int:pk>/marcar-leido/", views.notificacion_marcar_leido, name="notificacion_marcar_leido"),
    path("marcar-todas-leidas/", views.notificacion_marcar_todas_leidas, name="notificacion_marcar_todas_leidas"),
]
