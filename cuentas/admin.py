from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		("Datos extra", {"fields": ("nombre", "correo", "rol", "estado_cuenta", "fecha_registro")}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		("Datos extra", {"fields": ("nombre", "correo", "rol", "estado_cuenta", "fecha_registro")}),
	)

	list_display = ("correo", "nombre", "rol", "estado_cuenta", "is_staff", "is_superuser")
	ordering = ("correo",)

