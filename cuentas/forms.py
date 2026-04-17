from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import SolicitudBaja

Usuario = get_user_model()

class CrearUsuario(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'}),
    min_length=8,
    help_text="Mínimo 8 caracteres"
    )
    password_confirm = forms.CharField(label="Repite contraseña", widget=forms.PasswordInput(
        attrs={'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'}))
    
    class Meta:
        model = Usuario
        fields = ("nombre", "correo")
        labels = {
            "nombre": "Nombre completo",
            "correo": "Correo electrónico",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'
            }),
            "correo": forms.EmailInput(attrs={
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if Usuario.objects.filter(correo=correo).exists():
            raise ValidationError("Este correo ya está registrado")
        return correo

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        usuario.username = self.cleaned_data["correo"]
        if commit:
            usuario.save()
        return usuario


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("nombre",)
        labels = {
            "nombre": "Nombre completo",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;'
            }),
        }


class SolicitudBajaForm(forms.ModelForm):
    class Meta:
        model = SolicitudBaja
        fields = ("motivo",)
        labels = {
            "motivo": "Motivo de la solicitud (opcional)",
        }
        widgets = {
            "motivo": forms.Textarea(attrs={
                'placeholder': 'Cuéntanos por qué deseas darte de baja',
                'rows': 4,
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-family: Arial, sans-serif;'
            }),
        }


class ProcessarSolicitudBajaForm(forms.ModelForm):
    class Meta:
        model = SolicitudBaja
        fields = ("estado", "comentario_admin")
        labels = {
            "estado": "Decisión",
            "comentario_admin": "Comentarios (opcional)",
        }
        widgets = {
            "estado": forms.Select(attrs={
                'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;'
            }),
            "comentario_admin": forms.Textarea(attrs={
                'placeholder': 'Comentarios sobre la decisión',
                'rows': 3,
                'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-family: Arial, sans-serif;'
            }),
        }