from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ("id", "correo", "nombre", "rol", "is_staff", "is_active")
	search_fields = ("correo", "nombre")
	list_filter = ("rol", "is_staff", "is_active")
