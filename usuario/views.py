from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from usuario.models import Usuario
from notificaciones.services import crearNotificacion
from .forms import usuarioForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usu = form.save()
            login(request, usu)
            messages.success(request, f"Bienvendio {request.user.username}")
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuario/registro.html', {'form':form})

def iniciarSesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvendio {request.user.username}")
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'usuario/login.html')

def cerrarSesion(request):
    logout(request)
    return redirect('login')

def editarUsuario(request):
    usuario = request.user
    formUsername = usuarioForm(request.POST, request.FILES, instance=usuario)
    formContra = PasswordChangeForm(request.user, request.POST)

    if request.method == 'POST':
        if 'username' in request.POST:
            if formUsername.is_valid():
                usuario.username = request.POST['username']
                usuario.save()
                return redirect('perfil')

        elif formContra.is_valid():
            usuario = formContra.save()
            update_session_auth_hash(request, usuario)
            return redirect('perfil')

        elif 'eliminar' in request.POST:
            request.user.delete()
            return redirect('inicio')

    return render(request, 'usuario/perfil.html', {"formUsername":formUsername, "formContra":formContra, "usuario":usuario})