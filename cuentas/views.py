from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CrearUsuario, EditarPerfilForm, SolicitudBajaForm, ProcessarSolicitudBajaForm
from .models import Usuario, SolicitudBaja

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


@login_required
def perfil_view(request):
    """CU07 - Mostrar perfil del usuario autenticado"""
    usuario = request.user
    solicitud_baja = SolicitudBaja.objects.filter(usuario=usuario).first()
    
    return render(request, "cuentas/perfil.html", {
        "usuario": usuario,
        "solicitud_baja": solicitud_baja,
    })


@login_required
def editar_perfil_view(request):
    """CU07 - Editar perfil del usuario autenticado"""
    usuario = request.user
    
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect("perfil")
    else:
        form = EditarPerfilForm(instance=usuario)
    
    return render(request, "cuentas/editar_perfil.html", {
        "form": form,
        "usuario": usuario,
    })


@login_required
def solicitar_baja_view(request):
    """CU13 - Solicitar baja de cuenta"""
    usuario = request.user
    
    # Verificar si ya tiene solicitud pendiente o aprobada
    solicitud_existente = SolicitudBaja.objects.filter(
        usuario=usuario,
        estado__in=[SolicitudBaja.Estado.PENDIENTE, SolicitudBaja.Estado.APROBADA]
    ).first()
    
    if solicitud_existente:
        messages.warning(request, "Ya tienes una solicitud de baja en proceso")
        return redirect("perfil")
    
    if request.method == "POST":
        form = SolicitudBajaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = usuario
            solicitud.save()
            messages.success(request, "Solicitud de baja registrada. El equipo administrativo la revisará pronto.")
            return redirect("perfil")
    else:
        form = SolicitudBajaForm()
    
    return render(request, "cuentas/solicitar_baja.html", {
        "form": form,
        "usuario": usuario,
    })


@login_required
def solicitudes_baja_view(request):
    """CU14 - Panel admin para ver solicitudes de baja"""
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden acceder a este área")
        return redirect("inicio")
    
    estado = request.GET.get("estado", "").strip()
    qs = SolicitudBaja.objects.select_related("usuario", "admin_que_proceso")
    
    if estado:
        qs = qs.filter(estado=estado)
    else:
        # Por defecto mostrar PENDIENTE
        qs = qs.filter(estado=SolicitudBaja.Estado.PENDIENTE)
    
    qs = qs.order_by("-fecha_solicitud")
    
    return render(request, "cuentas/solicitudes_baja.html", {
        "solicitudes": qs,
        "estado": estado,
        "estados": SolicitudBaja.Estado.choices,
    })


@login_required
def procesar_solicitud_baja_view(request, pk):
    """CU14 - Procesar solicitud de baja (aprobar/rechazar)"""
    if not request.user.es_admin:
        messages.error(request, "No tienes permiso para esta acción")
        return redirect("inicio")
    
    solicitud = get_object_or_404(SolicitudBaja, pk=pk)
    
    if request.method == "POST":
        form = ProcessarSolicitudBajaForm(request.POST, instance=solicitud)
        if form.is_valid():
            solicitud_guardada = form.save(commit=False)
            solicitud_guardada.admin_que_proceso = request.user
            solicitud_guardada.fecha_procesamiento = timezone.now()
            
            # Si se aprueba, cambiar estado de cuenta del usuario
            if solicitud_guardada.estado == SolicitudBaja.Estado.APROBADA:
                usuario = solicitud.usuario
                usuario.estado_cuenta = Usuario.EstadoCuenta.PENDIENTE_ELIMINACION
                usuario.save()
                messages.success(request, f"Solicitud de {usuario.correo} aprobada. Cuenta marcada como pendiente de eliminación.")
            elif solicitud_guardada.estado == SolicitudBaja.Estado.RECHAZADA:
                messages.info(request, f"Solicitud de {solicitud.usuario.correo} rechazada.")
            
            solicitud_guardada.save()
            return redirect("solicitudes_baja")
    else:
        form = ProcessarSolicitudBajaForm(instance=solicitud)
    
    return render(request, "cuentas/procesar_solicitud_baja.html", {
        "solicitud": solicitud,
        "form": form,
    })