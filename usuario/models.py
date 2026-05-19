from django.db import models
from django.contrib.auth.models import AbstractUser

ESTADO = [('pendiente','Pendiente'), ('activa','Activa'), ('eliminada', 'Eliminada')]
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    fecha_registro = models.DateField(auto_now_add=True)
    estado_cuenta = models.CharField(max_length=100, choices=ESTADO, default='activa')

    def __str__(self):
        return f"{self.username}"