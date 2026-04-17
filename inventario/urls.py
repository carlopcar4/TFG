from django.urls import path
from . import views

urlpatterns = [
	path("arboles/", views.arbol_lista, name="arbol_lista"),
	path("arboles/crear/", views.arbol_crear, name="arbol_crear"),
	path("arboles/<int:pk>/", views.arbol_detalle, name="arbol_detalle"),
	path("arboles/<int:pk>/editar/", views.arbol_editar, name="arbol_editar"),
	path("alcorques/", views.alcorque_lista, name="alcorque_lista"),
	path("alcorques/crear/", views.alcorque_crear, name="alcorque_crear"),
	path("alcorques/<int:pk>/", views.alcorque_detalle, name="alcorque_detalle"),
	path("alcorques/<int:pk>/editar/", views.alcorque_editar, name="alcorque_editar"),
]
