from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Notificacion

@login_required
def notificacion_lista(request):
    """Lista de notificaciones del usuario actual (CU28)"""
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    sin_leer = notificaciones.filter(leido=False)
    
    return render(request, "notificaciones/notificacion_lista.html", {
        "notificaciones": notificaciones,
        "sin_leer_count": sin_leer.count(),
    })

@login_required
@require_http_methods(["POST"])
def notificacion_marcar_leido(request, pk):
    """Marcar una notificación como leída (CU28)"""
    notificacion = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
    notificacion.leido = True
    notificacion.save()
    messages.success(request, "Notificación marcada como leída")
    return redirect("notificacion_lista")

@login_required
@require_http_methods(["POST"])
def notificacion_marcar_todas_leidas(request):
    """Marcar todas las notificaciones como leídas (CU28)"""
    notificaciones = Notificacion.objects.filter(usuario=request.user, leido=False)
    count = notificaciones.update(leido=True)
    messages.success(request, f"{count} notificaciones marcadas como leídas")
    return redirect("notificacion_lista")
