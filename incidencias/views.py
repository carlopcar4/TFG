from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import IncidenciaForm, IncidenciaDetalleForm, IncidenciaFotoForm

from inventario.models import Arbol, Alcorque, Barrio
from .models import Incidencia
from cuentas.models import Usuario
from notificaciones.models import Notificacion


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
def incidencias_por_validar(request):
    """Vista para administradores: incidencias abiertas por validar (CU04)"""
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden acceder a este área")
        return redirect("incidencia_lista")
    
    qs = Incidencia.objects.select_related(
        "usuario", "admin_resp", "arbol", "alcorque"
    ).filter(estado=Incidencia.Estado.ABIERTA).order_by("-fecha_reporte")
    
    return render(request, "incidencias/incidencias_por_validar.html", {
        "incidencias": qs,
    })


@login_required
def incidencia_detalle(request, pk):
    incidencia = get_object_or_404(Incidencia.objects.select_related("usuario", "admin_resp", "arbol", "alcorque"), pk=pk)

    es_admin = getattr(request.user, "es_admin", False)
    
    # Solo el usuario autenticado o un admin pueden ver detalles
    if not es_admin and request.user != incidencia.usuario:
        messages.error(request, "No tienes permiso para ver esta incidencia")
        return redirect("incidencia_lista")
    
    # Obtener administradores válidos para asignar responsable
    grupo_admin = Group.objects.filter(name="Administradores").first()
    admins_validos = Usuario.objects.none()
    if grupo_admin:
        admins_validos = Usuario.objects.filter(groups=grupo_admin).order_by("correo")
    
    # Si es admin, mostrar formulario de detalle; si es usuario normal, mostrar solo lectura
    if es_admin:
        form = IncidenciaDetalleForm(instance=incidencia)
        form.fields["admin_resp"].queryset = admins_validos
        
        if request.method == "POST":
            form = IncidenciaDetalleForm(request.POST, instance=incidencia)
            form.fields["admin_resp"].queryset = admins_validos
            if form.is_valid():
                estado_anterior = incidencia.__class__.objects.get(pk=pk).estado
                incidencia = form.save(commit=False)
                
                # Crear notificación si el estado cambió (CU17)
                if incidencia.estado != estado_anterior:
                    Notificacion.crear_notificacion_cambio_estado(incidencia, incidencia.estado)
                    messages.info(request, f"Estado cambiado de {incidencia.get_estado_display()} a {incidencia.get_estado_display()}")
                
                incidencia.save()
                messages.success(request, "Cambios guardados correctamente")
                return redirect("incidencia_detalle", pk=incidencia.pk)
    else:
        form = None

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
    
    # Si ambos vienen en GET, prioriza árbol
    if arbol and alcorque:
        alcorque = None
    
    # Preparar initial data para el formulario
    initial_data = {}
    if arbol:
        initial_data['arbol'] = arbol.id
    if alcorque:
        initial_data['alcorque'] = alcorque.id
    
    if request.method == "POST":
        form = IncidenciaForm(request.POST, request.FILES)
        
        arbol_post = request.POST.get("arbol")
        alcorque_post = request.POST.get("alcorque")
        
        # Determina cuál elemento se seleccionó en el formulario
        arbol_form = None
        alcorque_form = None
        
        if arbol_post:
            arbol_form = get_object_or_404(Arbol, pk=arbol_post)
        if alcorque_post:
            alcorque_form = get_object_or_404(Alcorque, pk=alcorque_post)
        
        # Si ambos vienen del formulario, prioriza árbol
        if arbol_form and alcorque_form:
            alcorque_form = None
        
        # Usa del formulario si existen, si no usa del GET
        if arbol_form:
            arbol = arbol_form
        if alcorque_form:
            alcorque = alcorque_form
        
        # Validación: debe haber un elemento
        if not arbol and not alcorque:
            form.add_error(None, "Debes seleccionar un árbol o un alcorque.")
        
        if form.is_valid() and (arbol or alcorque):
            incidencia = form.save(commit=False)
            incidencia.usuario = request.user
            incidencia.arbol = arbol
            incidencia.alcorque = alcorque
            try:
                incidencia.save()
                messages.success(request, "Incidencia creada correctamente")
                return redirect("incidencia_lista")
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        # GET: crear formulario con valores iniciales
        form = IncidenciaForm(initial=initial_data)
    
    context = {
        "arbol": arbol,
        "alcorque": alcorque,
        "form": form,
    }
    return render(request, "incidencias/incidencia_nueva.html", context)


@login_required
def incidencia_editar_foto(request, pk):
    """Editar foto/evidencia de una incidencia existente - solo el reportador (CU39)"""
    incidencia = get_object_or_404(Incidencia.objects.select_related("usuario"), pk=pk)
    
    # Solo el usuario que reportó puede editar la foto
    if request.user != incidencia.usuario:
        messages.error(request, "Solo puedes editar la evidencia de tus propias incidencias")
        return redirect("incidencia_detalle", pk=pk)
    
    if request.method == "POST":
        form = IncidenciaFotoForm(request.POST, request.FILES, instance=incidencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Evidencia actualizada correctamente")
            return redirect("incidencia_detalle", pk=incidencia.pk)
    else:
        form = IncidenciaFotoForm(instance=incidencia)
    
    return render(request, "incidencias/incidencia_evidencia_form.html", {
        "form": form,
        "incidencia": incidencia,
    })


@login_required
def incidencias_por_barrio(request):
    """Ver incidencias agrupadas por barrio/zona (CU20) - solo administradores"""
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden ver este reporte")
        return redirect("incidencia_lista")
    
    # Obtener filtros
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    
    # Obtener todas las incidencias base
    incidencias_qs = Incidencia.objects.select_related(
        "usuario", "admin_resp", "arbol", "alcorque"
    )
    
    # Aplicar filtros si existen
    if estado:
        incidencias_qs = incidencias_qs.filter(estado=estado)
    
    if q:
        incidencias_qs = incidencias_qs.filter(
            Q(titulo__icontains=q) | Q(descripcion__icontains=q)
        )
    
    # Obtener todos los barrios con sus incidencias
    barrios = Barrio.objects.prefetch_related('arboles', 'alcorques').order_by("nombre")
    
    # Agrupar incidencias por barrio
    barrios_agrupados = []
    for barrio in barrios:
        # Incidencias del barrio (a través de árboles o alcorques)
        incidencias_barrio = incidencias_qs.filter(
            Q(arbol__barrio=barrio) | Q(alcorque__barrio=barrio)
        ).distinct().order_by("-fecha_reporte")
        
        if incidencias_barrio.exists():
            # Contar por estado
            conteos = {
                "total": incidencias_barrio.count(),
                "abierta": incidencias_barrio.filter(estado=Incidencia.Estado.ABIERTA).count(),
                "en_proceso": incidencias_barrio.filter(estado=Incidencia.Estado.EN_PROCESO).count(),
                "cerrada": incidencias_barrio.filter(estado=Incidencia.Estado.CERRADA).count(),
            }
            
            barrios_agrupados.append({
                "barrio": barrio,
                "incidencias": incidencias_barrio,
                "conteos": conteos,
            })
    
    return render(request, "incidencias/incidencias_por_barrio.html", {
        "barrios_agrupados": barrios_agrupados,
        "q": q,
        "estado": estado,
        "estados": Incidencia.Estado.choices,
    })

