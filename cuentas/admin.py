from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, SolicitudBaja

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


@admin.register(SolicitudBaja)
class SolicitudBajaAdmin(admin.ModelAdmin):
	list_display = ("id", "usuario", "estado", "fecha_solicitud", "admin_que_proceso")
	list_filter = ("estado", "fecha_solicitud")
	search_fields = ("usuario__correo", "usuario__nombre", "motivo")
	ordering = ("-fecha_solicitud",)
	readonly_fields = ("fecha_solicitud", "fecha_procesamiento", "admin_que_proceso")
	
	fieldsets = (
		("Solicitud", {
			"fields": ("usuario", "estado", "motivo")
		}),
		("Procesamiento", {
			"fields": ("admin_que_proceso", "comentario_admin")
		}),
		("Fechas", {
			"fields": ("fecha_solicitud", "fecha_procesamiento"),
			"classes": ("collapse",)
		}),
	)

