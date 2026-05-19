from django.contrib import admin
from .models import Incidencia

class AdminIncidencia(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'grado', 'estado', 'foto', 'elemento', 'admin_resp')
admin.site.register(Incidencia, AdminIncidencia)