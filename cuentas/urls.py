from django.urls import path
from . import views

urlpatterns= [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    path("perfil/editar/", views.editar_perfil_view, name="editar_perfil"),
    path("perfil/solicitar-baja/", views.solicitar_baja_view, name="solicitar_baja"),
    path("solicitudes-baja/", views.solicitudes_baja_view, name="solicitudes_baja"),
    path("solicitudes-baja/<int:pk>/procesar/", views.procesar_solicitud_baja_view, name="procesar_solicitud_baja"),
]