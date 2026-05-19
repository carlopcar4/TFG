from django.contrib import admin
from .models import Notificaciones

class AdminNotificaciones(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'incidencia', 'fecha', 'leida')
admin.site.register(Notificaciones, AdminNotificaciones)