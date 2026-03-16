from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import IncidenciaForm, IncidenciaDetalleForm

from inventario.models import Arbol, Alcorque
from .models import Incidencia
from cuentas.models import Usuario


@login_required
def incidencia_lista(request):
    qs = Incidencia.objects.select_related(
        "usuario", "admin_resp", "arbol", "alcorque"
    )
    
    if not request.user.es_admin:
        qs = qs.filter(usuario=request.user)
    
    estado = request.GET.get("estado", "").strip()
    q = request.GET.get("q", "").strip()
    
    if estado:
        qs = qs.filter(estado=estado)
    
    if q:
        qs = qs.filter(Q(titulo__icontains=q) | Q(descripcion__icontains=q))
        
    qs = qs.order_by("-fecha_reporte")
    
    return render(request, "incidencias/incidencia_lista.html", {
        "incidencias": qs,
        "estado": estado,
        "q": q
    })



@login_required
def incidencia_detalle(request, pk):
    incidencia = get_object_or_404(Incidencia.objects.select_related("usuario", "admin_resp", "arbol", "alcorque"), pk=pk)

    es_admin = getattr(request.user, "es_admin", False)
    grupo_admin = Group.objects.filter(name="Administradores").first()
    admins_validos = Usuario.objects.none()
    if grupo_admin:
        admins_validos = Usuario.objects.filter(groups=grupo_admin).order_by("correo")
        
    form = IncidenciaDetalleForm(instance=incidencia)
    form.fields["admin_resp"].queryset = admins_validos
    
    
    if request.method == "POST":
        form = IncidenciaDetalleForm(request.POST, instance=incidencia)
        form.fields["admin_resp"].queryset = admins_validos
        if not es_admin:
            messages.error(request, "No tienes permisos")
            return redirect("incidencia_detalle", pk=incidencia.pk)
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados")
            return redirect("incidencia_detalle", pk=incidencia.pk)

    return render(request, "incidencias/incidencia_detalle.html", {
        "incidencia": incidencia,
        "form": form,
        "es_admin": es_admin,
    })



@login_required
def incidencia_nueva(request):
    arbol_id = request.GET.get("arbol")
    alcorque_id = request.GET.get("alcorque")
    
    arbol = None
    alcorque = None
    
    if arbol_id:
        arbol = get_object_or_404(Arbol, pk=arbol_id)
    
    if alcorque_id:
        alcorque = get_object_or_404(Alcorque, pk=alcorque_id)
    
    if arbol and alcorque:
        alcorque = None
    
    form = IncidenciaForm()
    if request.method == "POST":
        form = IncidenciaForm(request.POST)

        arbol_post = request.POST.get("arbol")
        alcorque_post = request.POST.get("alcorque")

        if arbol is None and arbol_post:
            arbol = get_object_or_404(Arbol, pk=arbol_post)
        if alcorque is None and alcorque_post:
            alcorque = get_object_or_404(Alcorque, pk=alcorque_post)
        if arbol and alcorque:
            alcorque = None

        if arbol==None and alcorque==None:
            form.add_error(None, "No hay asociado árbol o alcorque, vete a la lista correspondiente y crea la incidencia desde él.")

        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.usuario = request.user
            incidencia.arbol = arbol
            incidencia.alcorque = alcorque
            try:
                incidencia.save()
                
            except ValidationError as a:
                form.add_error(None, a)
            else:
                messages.success(request, "Incidencia creada correctamente")
                return redirect("incidencia_lista")
    
    context = {
        "arbol": arbol,
        "alcorque": alcorque,
        "form": form,
    }
    return render(request, "incidencias/incidencia_nueva.html", context)

