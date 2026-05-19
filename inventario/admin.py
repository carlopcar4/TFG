from django.contrib import admin
from .models import Elemento, Barrio, Especie

class AdminElemento(admin.ModelAdmin):
    list_display = ('tipo', 'especie', 'barrio', 'estado', 'latitud', 'longitud','direccion','fecha_plant', 'potencial_plant')
admin.site.register(Elemento,AdminElemento)

class AdminBarrio(admin.ModelAdmin):
    list_display = ('nombre', 'delimitacion')
admin.site.register(Barrio,AdminBarrio)

class AdminEspecie(admin.ModelAdmin):
    list_display = ('nombre_comun', 'nombre_cient', 'familia')
admin.site.register(Especie,AdminEspecie)
