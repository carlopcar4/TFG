from django.contrib import admin
from .models import Barrio, Especie, Arbol, Alcorque

@admin.register(Arbol)
class ArbolAdmin(admin.ModelAdmin):
    list_display = ("id", "especie", "barrio", "estado", "direccion", "latitud",
                "longitud", "fecha_plant")

    list_filter = ("estado", "barrio", "especie")
    search_fields = ("direccion", "especie__nombre_comun", "barrio__nombre")
    ordering = ("-id",)
    list_per_page = 25
    list_select_related = ("especie", "barrio")


@admin.register(Alcorque)
class AlcorqueAdmin(admin.ModelAdmin):
    list_display = ("id", "barrio", "estado", "direccion", "latitud",
                "longitud")
    
    list_filter = ("estado", "barrio")
    search_fields = ("direccion", "barrio__nombre")
    ordering = ("-id",)
    list_per_page = 25
    list_select_related = ("barrio",)


@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    search_fields = ("nombre_comun", "nombre_cient", "familia")