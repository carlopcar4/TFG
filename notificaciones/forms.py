from django import forms
from .models import Notificacion

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ("leido",)
        labels = {
            "leido": "Marcar como leído",
        }
