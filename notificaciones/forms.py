from django import forms
from .models import Notificaciones

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificaciones
        fields = ('leida',)