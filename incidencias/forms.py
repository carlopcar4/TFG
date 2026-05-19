from django import forms
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ('titulo', 'descripcion', 'grado', 'foto', 'elemento')

class incidenciaCambioForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ('grado', 'estado', 'admin_resp')