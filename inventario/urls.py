from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.Arboles.as_view(), name='arboles'),
    path('especies/', views.Especies.as_view(),name='especies'),
    path('especies/nueva', views.especieNueva, name='especieNueva'),
    path('barrios/',views.Barrios.as_view(),name='barrios'),
    path('barrios/nuevo', views.barrioNuevo, name='barrioNuevo'),
    path('nuevo/', views.añadirArbol, name='añadirArbol'),
    path('<int:pk>', views.ArbolDetalle.as_view(), name='arbolDetalle'),
    path('<int:pk>/editar/', views.arbolEditar, name='arbolEditar'),
] + static(settings.STATIC_URL)
