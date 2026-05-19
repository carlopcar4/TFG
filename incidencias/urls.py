from django.urls import path
from . import views


urlpatterns = [
    path('nueva/', views.incidenciaNueva, name='nueva'),
    path('', views.listarIncidencias.as_view(), name='listarIncidencias'),
    path('<int:pk>/', views.editarIncidencia, name='detalleIncidencia'),
    ]
