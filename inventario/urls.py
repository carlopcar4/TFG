from django.urls import path
from . import views

urlpatterns = [
	path("arboles/", views.arbol_lista, name="arbol_lista"),
]
