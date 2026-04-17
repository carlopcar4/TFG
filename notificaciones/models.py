from django.db import models
from django.utils import timezone

class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        ESTADO_CAMBIO = "ESTADO_CAMBIO", "Cambio de estado"
        ASIGNACION = "ASIGNACION", "Asignación de responsable"

    usuario = models.ForeignKey("cuentas.Usuario", on_delete=models.CASCADE, related_name="notificaciones")
    incidencia = models.ForeignKey("incidencias.Incidencia", on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=30, choices=Tipo.choices, default=Tipo.ESTADO_CAMBIO)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name_plural = "notificaciones"

    def __str__(self):
        return f"Notificación para {self.usuario.nombre}: {self.get_tipo_display()}"

    @classmethod
    def crear_notificacion_cambio_estado(cls, incidencia, nuevo_estado):
        """Crear notificación cuando la incidencia cambia de estado"""
        mensaje = f"Tu incidencia '{incidencia.titulo}' ha cambiado a {incidencia.get_estado_display()}"
        return cls.objects.create(
            usuario=incidencia.usuario,
            incidencia=incidencia,
            tipo=cls.Tipo.ESTADO_CAMBIO,
            mensaje=mensaje
        )
