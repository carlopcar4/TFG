from .models import Notificaciones

def crearNotificacion(usuario, tipo, incidencia=None):
    return Notificaciones.objects.create(usuario=usuario, tipo=tipo, incidencia=incidencia)