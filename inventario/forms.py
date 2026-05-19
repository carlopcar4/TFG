from django import forms
from .models import Elemento, Barrio, Especie

class elementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['tipo', 'especie', 'potencial_plant', 'estado','observaciones', 'fecha_plant']

class elementoNuevoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['tipo','barrio','especie','estado','latitud','longitud','direccion','fecha_plant','potencial_plant']

class elementoNuevoArbolForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['tipo','barrio','especie','estado','latitud','longitud','direccion','fecha_plant','potencial_plant']

class elementoNuevoAlcorqForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['tipo','barrio','estado','latitud','longitud','direccion','potencial_plant']

class nuevaEspecie(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nombre_comun', 'nombre_cient', 'familia', 'descripcion']

class nuevoBarrio(forms.ModelForm):
    class Meta:
        model = Barrio
        fields = ['nombre', 'delimitacion']

class editarElemForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['tipo','barrio','especie','estado','latitud','longitud','direccion','fecha_plant','potencial_plant']
