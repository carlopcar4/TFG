from django import forms
from .models import Arbol, Alcorque

class ArbolForm(forms.ModelForm):
    class Meta:
        model = Arbol
        fields = ("especie", "barrio", "estado", "latitud", "longitud", "direccion", "fecha_plant", "observaciones")
        labels = {
            "especie": "Especie",
            "barrio": "Barrio",
            "estado": "Estado",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "direccion": "Dirección",
            "fecha_plant": "Fecha de plantación",
            "observaciones": "Observaciones",
        }
        widgets = {
            "direccion": forms.Textarea(attrs={"rows": 3, "placeholder": "Dirección del árbol"}),
            "observaciones": forms.Textarea(attrs={"rows": 3, "placeholder": "Observaciones opcionales"}),
            "fecha_plant": forms.DateInput(attrs={"type": "date"}),
            "latitud": forms.NumberInput(attrs={"step": "0.000001"}),
            "longitud": forms.NumberInput(attrs={"step": "0.000001"}),
        }

class AlcorqueForm(forms.ModelForm):
    class Meta:
        model = Alcorque
        fields = ("barrio", "estado", "potencial_plant", "latitud", "longitud", "direccion", "observaciones")
        labels = {
            "barrio": "Barrio",
            "estado": "Estado",
            "potencial_plant": "Potencial de plantación",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "direccion": "Dirección",
            "observaciones": "Observaciones",
        }
        widgets = {
            "direccion": forms.Textarea(attrs={"rows": 3, "placeholder": "Dirección del alcorque"}),
            "observaciones": forms.Textarea(attrs={"rows": 3, "placeholder": "Observaciones opcionales"}),
            "latitud": forms.NumberInput(attrs={"step": "0.000001"}),
            "longitud": forms.NumberInput(attrs={"step": "0.000001"}),
        }
