from django.db import models
from usuario.models import Usuario
from incidencias.models import Incidencia

class NotificacionTipo(models.TextChoices):
    INCIDENCIA_CREADA = 'INCIDENCIA_CREADA', 'Incidencia creada correctamente'
    INCIDENCIA_MODIFICADA = 'INCIDENCIA_MODIFICADA', 'Su incidencia ha sido actualizada'
    INCIDENCIA_RESPONSABLE = 'INCIDENCIA_RESPONSABLE', 'Has sido seleccionado como responsable para una incidencia'
    ESTADO = 'ESTADO', 'Cambio de estado'
    SISTEMA = 'SISTEMA', 'Aviso del sistema'
    PERFIL_MODIFICAD = 'PERFIL_MODIFICAD', '¡Su perfil ha sido modificado correctamente!'

class Notificaciones(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificado')
    tipo = models.CharField(max_length=30, choices=NotificacionTipo)
    incidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    def __str__(self):
        return f"#{self.usuario} - #{self.tipo}"