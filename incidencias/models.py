from django.db import models
from usuario.models import Usuario
from inventario.models import Elemento

GRADO = [('leve','Leve'),('medio','Medio'),('grave','Grave'), ('urgente', 'Urgente')]
ESTADO = [('pendiente','Pendiente'),('abierta','Abierta'),('en_proceso','En proceso'),('cerrada','Cerrada')]

class Incidencia(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    grado = models.CharField(max_length=30, choices=GRADO, default='leve')
    fecha_reporte = models.DateField(auto_now_add=True)
    fecha_act = models.DateField(auto_now=True)
    estado = models.CharField(max_length=30, choices=ESTADO, default='pendiente')
    foto = models.ImageField(upload_to='incidencias/', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="creador")
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, blank=True, null=True)
    admin_resp = models.ForeignKey(Usuario, on_delete=models.PROTECT, blank=True, null=True, related_name="admin_responsable", limit_choices_to={'is_staff': True})
    
    def __str__(self):
        return f"Incidencia #{self.id}: #{self.titulo}"