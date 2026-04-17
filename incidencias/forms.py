from django import forms
from .models import Incidencia
from inventario.models import Arbol, Alcorque

class IncidenciaForm(forms.ModelForm):
    arbol = forms.ModelChoiceField(
        queryset=Arbol.objects.all(),
        required=False,
        label="Árbol",
        empty_label="-- Seleccionar árbol --"
    )
    alcorque = forms.ModelChoiceField(
        queryset=Alcorque.objects.all(),
        required=False,
        label="Alcorque",
        empty_label="-- Seleccionar alcorque --"
    )
    
    class Meta:
        model = Incidencia
        fields = ("titulo", "descripcion", "grado_incidencia", "arbol", "alcorque", "foto")
        labels = {
            "titulo": "Título",
            "descripcion": "Descripción",
            "grado_incidencia": "Grado de incidencia",
            "foto": "Fotografía (opcional)",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Resumen breve del problema"}),
            "descripcion": forms.Textarea(attrs={"placeholder": "Detalles de la incidencia", "rows": 5}),
        }

class IncidenciaDetalleForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ("estado", "admin_resp", "observaciones_internas")
        labels = {
            "estado": "Estado",
            "admin_resp": "Responsable",
            "observaciones_internas": "Observaciones internas (solo para administradores)",
        }
        widgets = {
            "observaciones_internas": forms.Textarea(attrs={
                "placeholder": "Notas privadas para el equipo administrativo",
                "rows": 4
            }),
        }

class IncidenciaFotoForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ("foto",)
        labels = {
            "foto": "Fotografía / Evidencia",
        }
        widgets = {
            "foto": forms.FileInput(attrs={"accept": "image/*"}),
        }