from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
	class Rol(models.TextChoices):
		REGISTRADO = "REGISTRADO", "Registrado"
		ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

	class EstadoCuenta(models.TextChoices):
		ACTIVA = "ACTIVA", "Activa"
		PENDIENTE_ELIMINACION = "PENDIENTE_ELIMINACION", "Pendiente eliminación"
		ELIMINADA = "ELIMINADA", "Eliminada"

	nombre = models.CharField(max_length=159)
	correo = models.EmailField(unique=True)
	rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.REGISTRADO,)
	fecha_registro = models.DateTimeField(default=timezone.now)
	estado_cuenta = models.CharField(max_length=30, choices=EstadoCuenta.choices, default=EstadoCuenta.ACTIVA)
	USERNAME_FIELD = "correo"
	REQUIRED_FIELDS = ["username"]

	@property
	def es_admin(self) -> bool:
		return self.rol == self.Rol.ADMINISTRADOR

	def save(self, *args, **kwargs):
		es_admin = (self.rol == self.Rol.ADMINISTRADOR)
		self.is_staff = es_admin
		super().save(*args, **kwargs)
		grupo_admin, _ = Group.objects.get_or_create(name="Administradores")
		if es_admin:
			self.groups.add(grupo_admin)
		else:
			self.groups.remove(grupo_admin)

	def __str__(self):
		return f"{self.nombre} ({self.correo})"


