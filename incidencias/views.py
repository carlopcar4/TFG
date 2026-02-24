from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import Group

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



def incidencia_detalle(request, pk):
    incidencia = get_object_or_404(
        Incidencia.objects.select_related("usuario", "admin_resp", "arbol", "alcorque"),
        pk=pk
    )
    
    errores = {}
    es_admin = getattr(request.user, "es_admin", False)
    
    grupo_admin = Group.objects.filter(name="Administradores").first()
    admins_validos = Usuario.objects.none()
    if grupo_admin:
        admins_validos = Usuario.objects.filter(groups=grupo_admin).order_by("correo")
    
    if request.method == "POST":
        if not es_admin:
            errores = {"general": ["No tienes permisos para modificar esta incidencia."]}
        else:
            estado = request.POST.get("estado", "").strip()
            admin_resp_id = request.POST.get("admin_resp", "").strip()

            if estado:
                incidencia.estado = estado
                
            if admin_resp_id == "":
                incidencia.admin_resp = None
            elif admin_resp_id.isdigit():
                candidato = Usuario.objects.filter(pk=int(admin_resp_id)).first()
                incidencia.admin_resp = candidato
                
            try:
                incidencia.save()
                return redirect("incidencia_detalle", pk=incidencia.id)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    errores = e.message_dict
                else:
                    errores = {"general": e.message}
                    
    return render(request, "incidencias/incidencia_detalle.html",{
        "incidencia": incidencia,
        "estados": Incidencia.Estado.choices,
        "admins_validos": admins_validos,
        "errores": errores,
        "es_admin": es_admin,
    })



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
    
    errores = {}
    
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        grado_incidencia = request.POST.get("grado_incidencia", Incidencia.GRADO.LEVE)
        
        arbol_post = request.POST.get("arbol")
        alcorque_post = request.POST.get("alcorque")
        
        arbol = Arbol.objects.filter(pk=arbol_post).first() if arbol_post else None
        alcorque = Alcorque.objects.filter(pk=alcorque_post).first() if alcorque_post else None
        
        incidencia = Incidencia(
            titulo=titulo,
            descripcion=descripcion,
            grado_incidencia=grado_incidencia,
            usuario=request.user,
            arbol=arbol,
            alcorque=alcorque,
        )
        
        try:
            incidencia.save()
            return redirect("/incidencias/")
        except ValidationError as e:
            if hasattr(e, "message_dict"):
                errores = e.message_dict
            else:
                errores = {"general": e.message}
    
    context = {
        "arbol": arbol,
        "alcorque": alcorque,
        "grados": Incidencia.Grado.choices,
        "errores": errores,
    }
    return render(request, "incidencias/incidencia_nueva.html", context)

