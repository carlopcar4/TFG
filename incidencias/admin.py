from django.contrib import admin
from .models import Incidencia

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
	list_display=("id", "titulo", "estado", "grado_incidencia", "usuario", "admin_resp", "fecha_reporte", 
		"fecha_act", "get_objetivo",)

	list_filter = ("estado", "grado_incidencia", "fecha_reporte")
	search_fields = ("titulo", "descripcion", "usuario__username")
	ordering = ("-fecha_reporte",)
	readonly_fields = ("fecha_reporte", "fecha_act")

	def get_objetivo(self, obj):
		if obj.arbol_id is not None:
			return f"Árbol #{obj.arbol_id}"
		if obj.alcorque_id is not None:
			return f"Alcroque #{obj.alcorque_id}"
		return "-"

	get_objetivo.short_description = "Objetivo"
