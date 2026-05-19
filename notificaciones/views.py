from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notificaciones
from django.shortcuts import get_object_or_404

@login_required
def misNotificaciones(request):
    notificaciones = Notificaciones.objects.filter(usuario=request.user)
    return render(request, 'notificaciones.html', {'notificaciones': notificaciones})

def eliminarNoti(request, pk):
    noti = get_object_or_404(Notificaciones, pk=pk)
    if request.method == "POST":
        noti.delete()
    return redirect('notificaciones')