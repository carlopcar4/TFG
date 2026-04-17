from django.contrib import admin
from .models import Incidencia

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
	list_display=("id", "titulo", "estado", "grado_incidencia", "usuario", "admin_resp", "fecha_reporte", 
		"fecha_act", "objeto",)

	list_filter = ("estado", "grado_incidencia", "fecha_reporte")
	search_fields = ("titulo", "descripcion", "usuario__correo", "admin_resp__correo", "observaciones_internas")
	ordering = ("-fecha_reporte",)
	readonly_fields = ("fecha_reporte", "fecha_act")

	fieldsets = (
		("Información de la incidencia", {
			"fields": ("titulo", "descripcion", "grado_incidencia", "estado", "foto")
		}),
		("Relaciones", {
			"fields": ("usuario", "arbol", "alcorque", "admin_resp")
		}),
		("Gestión administrativa", {
			"fields": ("observaciones_internas",)
		}),
		("Fechas", {
			"fields": ("fecha_reporte", "fecha_act"),
			"classes": ("collapse",)
		}),
	)

	def objeto(self, obj):
		if obj.arbol_id:
			return f"Árbol #{obj.arbol_id}"
		if obj.alcorque_id:
			return f"Alcorque #{obj.alcorque_id}"
		return "-"

	objeto.short_description = "Elemento"
