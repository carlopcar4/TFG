from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

class usuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username',)

