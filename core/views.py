from django.shortcuts import render
from incidencias.models import Incidencia
from inventario.models import Arbol, Alcorque

def inicio(request):
    arboles = list(Arbol.objects.values("id", "latitud", "longitud"))
    alcorques = list(Alcorque.objects.values("id", "latitud", "longitud"))
    
    context = {
        "arboles": arboles,
        "alcorques": alcorques,
    }
    return render(request, "core/inicio.html", context)