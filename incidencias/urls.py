from django.urls import path
from . import views

urlpatterns = [
	path("", views.incidencia_lista, name="incidencia_lista"),
	path("por-validar/", views.incidencias_por_validar, name="incidencias_por_validar"),
	path("por-barrio/", views.incidencias_por_barrio, name="incidencias_por_barrio"),
	path("nueva/", views.incidencia_nueva, name="nueva_incidencia"),
	path("<int:pk>/", views.incidencia_detalle, name="incidencia_detalle"),
	path("<int:pk>/editar-evidencia/", views.incidencia_editar_foto, name="incidencia_editar_foto"),
]