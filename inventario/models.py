from django.db import models
from django.core.exceptions import ValidationError

TIPO = [('arbol', 'Árbol'), ('alcorque', 'Alcorque')]
ESTADO = [('bueno','Bueno'), ('regular','Regular'), ('malo','Malo'), ('urgente','Urgente')]
POTENCIAL = [('apto','Apto'), ('no_apto','No apto')]

class Barrio(models.Model):
    nombre = models.CharField(max_length=50)
    delimitacion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nombre}"

class Especie(models.Model):
    nombre_comun = models.CharField(max_length=50)
    nombre_cient = models.CharField(max_length=50)
    familia = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nombre_comun}"

class Elemento(models.Model):
    tipo = models.CharField(max_length=30, choices=TIPO, default='arbol')
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.CharField(max_length=30, choices=ESTADO, default='bueno')
    latitud = models.DecimalField(max_digits=22, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=22, decimal_places=7, null=True, blank=True)
    direccion = models.CharField(max_length=40, blank=True)
    fecha_plant = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    potencial_plant = models.CharField(max_length=30, choices=POTENCIAL, default='apto', null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.tipo == 'arbol':
            if not self.especie:
                raise ValidationError({'especie': 'La especie es obligatoria para un árbol.'})
            if not self.fecha_plant:
                raise ValidationError({'fecha_plant': 'la fecha de plantación debe actualizarse'})
            self.potencial_plant = None
        elif self.tipo == 'alcorque':
            if not self.potencial_plant:
                raise ValidationError({'potencial_plant':'Es necesario saber si es potencialmente plantable'})
            self.especie = None
            self.fecha_plant = None
    
    def __str__(self):
        return f"{self.id} - {self.tipo} - {self.barrio}"