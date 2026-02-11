from django.db import models
from django.db.models import Q


class Especie(models.Model):
	nombre_comun = models.CharField(max_length=100)
	nombre_cient = models.CharField(max_length=100)
	familia = models.CharField(max_length=100)
	descripcion = models.TextField()


class Barrio(models.Model):
	nombre = models.CharField(max_length=100)
	delimitacion = models.TextField()


class Arbol(models.Model):

	class Estado(models.TextChoices):
		BUENO = "BUENO", "Bueno"
		REGULAR = "REGULAR", "Regular"
		MALO = "MALO", "Malo"
		NECESITA_INTERVENCION = "NECESITA_INTERVENCION", "Necesita intervención"

	especie = models.ForeignKey(Especie, on_delete=models.PROTECT, related_name="arboles")
	barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT, related_name="barrio_arbol")
	estado = models.CharField(max_length=80, choices=Estado.choices, default=Estado.BUENO)
	latitud = models.Decimal(max_digits=9, decimal_places=6, null=True, blank=True)
	longitud = models.Decimal(max_digits=9, decimal_places=6, null=True, blank=True)
	direccion = models.CharField(max_length=255, blank=True)
	fecha_plantacion = models.DateTimeField(null=True, blank=True)
	observaciones = models.TextField(blank=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["latitud", "longitud"],
				condition=Q(latitud__isnull=False, longitud__isnull=False),
				name="unq_arbol_lat_lon",
			),
			models.CheckConstraint(
				check=(Q(latitud__isnull=True, longitud__isnull=True | 
					Q(latitud__isnull=False, longitud__isnull=False)),
				name="lat_lon_par"
			),
		]

	def __str__(self):
		return f"Árbol #{self.id} ({self.especie.nombre_comun})"

class Alcorque(models.Model):

	class Estado(models.TextChoices):
		BUENO = "BUENO", "Bueno"
		REGULAR = "REGULAR", "Regular"
		MALO = "MALO", "Malo"
		NECESITA_INTERVENCION = "NECESITA_INTERVENCION", "Necesita intervención"

	class PotPlant(models.TextChoices):
		APTO = "APTO", "Apto"
		NO_APTO = "NO_APTO", "No apto"

	barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT, related_name="barrio_alcorque")
	estado = models.CharField(max_length=80, choices=Estado.choices, default=Estado.BUENO)
	potencial_plant = models.CharField(max_length=15, choices=PotPlant.choices, default=PotPlant.NO_APTO)
	latitud = models.Decimal(max_digits=9, decimal_places=6, null=True, blank=True)
	longitud = models.Decimal(max_digits=9, decimal_places=6, null=True, blank=True)
	direccion = models.CharField(max_length=255, blank=True)
	observaciones = models.TextField(blank=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["latitud", "longitud"],
				condition=Q(latitud__isnull=False, longitud__isnull=False),
				name="unq_alcorque_lat_lon",
			),
			models.CheckConstraint(
				check=(Q(latitud__isnull=True, longitud__isnull=True | 
					Q(latitud__isnull=False, longitud__isnull=False)),
				name="lat_lon_par"
			),
		]


	def __str__(self):
		return f"Alcorque #{self.id}"

