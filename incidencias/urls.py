from django.urls import path
from . import views

urlpatterns = [
	path("", views.incidencia_lista, name="incidencia_lista"),
	path("nueva/", views.incidencia_nueva, name="nueva_incidencia"),
	path("<int:pk>/", views.incidencia_detalle, name="incidencia_detalle"),


]