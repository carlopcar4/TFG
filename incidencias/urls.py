from django.urls import path
from . import views

urlpatterns = [
	path("nueva/", views.incidencia_nueva, name="nueva_incidencia"),


]