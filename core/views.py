from django.shortcuts import render
from inventario.models import Elemento, Especie

def inicio(request):
    elementos = Elemento.objects.all()
    especies = Especie.objects.all()
    return render(request, "core/inicio.html",{'elementos': elementos, 'especies': especies,})