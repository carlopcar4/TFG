from django.db import models

class Barrio(models.Model):
	nombre = models.CharField(max_length=100)
	delimitacion = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.nombre


class Especie(models.Model):
	nombre_comun = models.CharField(max_length=50)
	nombre_cient = models.CharField(max_length=50, null=True, blank=True)
	familia = models.CharField(max_length=50, null=True, blank=True)
	descripcion = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.nombre_comun


class Arbol(models.Model):
	class Estado(models.TextChoices):
		BUENO = "BUENO", "Bueno"
		REGULAR = "REGULAR", "Regular"
		MALO = "MALO", "Malo"
		NECESITA_INTERVENCION = "NECESITA_INTERVENCION", "Necesita intervención"

	especie = models.ForeignKey("inventario.Especie", on_delete=models.PROTECT, related_name="arboles",)
	barrio = models.ForeignKey("inventario.Barrio", on_delete=models.PROTECT, related_name="arboles",)
	estado = models.CharField(max_length=50, choices=Estado.choices, default=Estado.BUENO)
	latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	direccion = models.TextField(null=True, blank=True)
	fecha_plant = models.DateTimeField(null=True, blank=True)
	observaciones = models.TextField(null=True, blank=True)

	class Meta: constraints = [
		models.UniqueConstraint(fields=["latitud", "longitud"], name="un_arbol_por_ubi",)]

	def __str__(self):
		return f"Árbol #{self.id}"


class Alcorque(models.Model):
	class Estado(models.TextChoices):
		BUENO = "BUENO", "Bueno"
		REGULAR = "REGULAR", "Regular"
		MALO = "MALO", "Malo"
		NECESITA_INETRVENCION = "NECESITA_INTERVENCION", "Necesita intervención"

	class Potencial(models.TextChoices):
		APTO = "APTO", "Apto"
		NO_APTO = "NO_APTO", "No apto"

	barrio = models.ForeignKey("inventario.Barrio", on_delete=models.PROTECT, related_name="alcorque",)
	estado = models.CharField(max_length=50, choices=Estado.choices, default=Estado.BUENO)
	latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	direccion = models.TextField(null=True, blank=True)
	observaciones = models.TextField(null=True, blank=True)

	class Meta: constraints = [
                models.UniqueConstraint(fields=["latitud", "longitud"], name="un_alcorque_por_ubi",)]

	def __str__(self):
                return f"Alcorque #{self.id}"

