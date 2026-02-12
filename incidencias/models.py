from django.db import models
from django.db.models import Q

class Incidencia(models.Model):
	class Grado(models.TextChoices):
		LEVE = "LEVE", "Leve"
		MEDIO = "MEDIO", "Medio"
		GRAVE = "GRAVE", "Grave"

	class Estado(models.TextChoices):
		ABIERTA = "ABIERTA", "Abierta"
		EN_PROCESO = "EN_PROCESO", "En proceso"
		CERRADA = "CERRADA", "Cerrada"

	titulo = models.CharField(max_length=120)
	descripcion = models.TextField()
	grado_incidencia = models.CharField(max_length=30, choices=Grado.choices, default=Grado.LEVE)
	fecha_reporte = models.DateTimeField(auto_now_add=True)
	fecha_act = models.DateTimeField(auto_now=True, null=True, blank=True)
	estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.ABIERTA)
	foto_url = models.TextField(null=True, blank=True)
	usuario = models.ForeignKey("cuentas.Usuario", on_delete=models.PROTECT, related_name="usu_incidencia")
	arbol = models.ForeignKey("inventario.Arbol", on_delete=models.PROTECT, null=True, blank=True, related_name="arbol_inci")
	alcorque = models.ForeignKey("inventario.Alcorque", on_delete=models.PROTECT, null=True, blank=True, related_name="alcorque_inci")
	admin_resp = models.ForeignKey("cuentas.Usuario", on_delete=models.PROTECT, null=True, blank=True, related_name="admin_inci")

	class Meta: constraints = [
		models.CheckConstraint(check=(
			(Q(arbol__isnull=False) & Q(alcorque__isnull=True)) |
			(Q(arbol__isnull=True) & Q(alcorque__isnull=False))),
		name="check_arbol_alcorque_incidencia",),]

	def __str__(self):
		return f"Incidencia #{self.id}"
