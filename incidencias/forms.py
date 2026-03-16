from django import forms
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ("titulo", "descripcion", "grado_incidencia")

class IncidenciaDetalleForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ("estado", "admin_resp")