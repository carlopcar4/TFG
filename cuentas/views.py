from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CrearUsuario
from .models import Usuario

def signup(request):
    if request.user.is_authenticated:
        return redirect("arbol_lista")
    if request.method == "POST":
        form = CrearUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("inicio")
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, str(error))
            # for field, errors in form.errors.items():
            #     for error in errors:
            #         messages.error(request, f"{error}")
    else:
        form = CrearUsuario()

    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("arbol_lista")

    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        usuario = authenticate(request, username=correo, password=password)
        
        if usuario:
            login(request, usuario)
            return redirect("inicio")
        else:
            messages.error(request, "Correo o contraseña incorrectos")

    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return redirect("inicio")