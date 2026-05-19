from django.shortcuts import render, redirect
from .forms import IncidenciaForm
from .models import GRADO, ESTADO
from inventario.models import Elemento, Barrio
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from .models import Incidencia
from .forms import IncidenciaForm, incidenciaCambioForm
from notificaciones.services import crearNotificacion
from django.shortcuts import get_object_or_404
from usuario.models import Usuario
from inventario.models import Elemento



@login_required
def incidenciaNueva(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.usuario = request.user
            incidencia.elemento = Elemento.objects.get(id=request.GET.get('arbol'))
            incidencia.save()
            crearNotificacion(incidencia.usuario, "INCIDENCIA_CREADA", incidencia=incidencia)
            return redirect('listarIncidencias')
    else:
        form = IncidenciaForm()
    arboles = Elemento.objects.all()
    return render(request, 'incidencias/nueva.html', {'form':form,'grados':GRADO,'arboles':arboles})

class listarIncidencias(LoginRequiredMixin, ListView):
    template_name = 'incidencias/listarIncidencias.html'
    context_object_name = 'incidencias'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            incidencias = Incidencia.objects.all()
        else:
            incidencias = Incidencia.objects.filter(usuario=self.request.user)
        
        estado = self.request.GET.get('estado')
        grado = self.request.GET.get('grado')
        barrio = self.request.GET.get('barrio')
        if estado:
            incidencias = incidencias.filter(estado=estado)
        if grado:
            incidencias = incidencias.filter(grado=grado)
        if barrio:
            incidencias = incidencias.filter(elemento__barrio_id=barrio)
        return incidencias
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ESTADO
        context['grados'] = GRADO
        context['barrios'] = Barrio.objects.all()
        return context 

def editarIncidencia(request, pk):
    incidencia = get_object_or_404(Incidencia, pk=pk)
    if request.user.is_staff:
        admins = Usuario.objects.filter(is_staff=True)
    else:
        admins = None
    if request.method == 'POST':
        form = incidenciaCambioForm(request.POST, instance=incidencia)
        
        if form.is_valid():
            incidencia = form.save()
            crearNotificacion(incidencia.usuario, "INCIDENCIA_MODIFICADA", incidencia=incidencia)
            return redirect('listarIncidencias')
        elif 'eliminar' in request.POST:
            Incidencia.objects.filter(id=pk).delete()
            return redirect('listarIncidencias')
    else:
        form = incidenciaCambioForm()
    return render(request, 'incidencias/detalle.html',{"form":form,"incidencia":incidencia, "admins":admins, "grados":GRADO, "estados":ESTADO})
