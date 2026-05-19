from django.contrib import admin
from .models import Usuario

class AdminUsuario(admin.ModelAdmin):
    list_display = ('username', 'email', 'fecha_registro', 'estado_cuenta')
admin.site.register(Usuario, AdminUsuario)