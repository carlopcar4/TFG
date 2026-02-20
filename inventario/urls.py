from django.urls import path
from . import views

urlpatterns = [
	path("arboles/", views.arbol_lista, name="arbol_lista"),
	path("alcorques/", views.alcorque_lista, name="alcorque_lista"),
	path("arboles/<int:pk>", views.arbol_detalle, name="arbol_detalle"),
	path("alcorques/<int:pk>", views.alcorque_detalle, name="alcorque_detalle"),


]
