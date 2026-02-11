from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

class UsuarioManager(BaseUserManager):
	def create_user(self, correo, password=None, **extra_fields):
		if not correo: raise ValueError("El correo es obligatorio")
		correo = self.normalize_email(correo)
		user = self.model(correo=correo, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, correo, password=None, **extra_fields):
		extra_fields.setdefault("rol", Usuario.Rol.ADMINISTRADOR)
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("estado_cuenta", Usuario.EstadoCuenta.ACTIVA)
		return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
	class Rol(models.TextChoices):
		REGISTRADO = "REGISTRADO", "Registrado"
		ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

	class EstadoCuenta(models.TextChoices):
		ACTIVA = "ACTIVA", "Activa"
		PENDIENTE_ELIMINACION = "PENDIENTE_ELIMINACION", "Pendiente eliminación"
		ELIMINADA = "ELIMINADA", "Eliminada"

	nombre = models.CharField(max_length=80)
	correo = models.EmailField(max_length=120, unique=True)
	rol = models.CharField(max_length=80, choices=Rol.choices, default=Rol.REGISTRADO)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	estado_cuenta = models.CharField(max_length=25, choices=EstadoCuenta.choices, default=EstadoCuenta.ACTIVA)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UsuarioManager()

	USERNAME_FIELD = "correo"
	REQUIRED_FIELDS = ["nombre"]

	def __str__(self):
		return f"{self.nombre} <{self.correo}>"
