from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Arbol, Alcorque, Barrio, Especie
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArbolForm, AlcorqueForm

def arbol_lista(request):
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    barrio_id = request.GET.get("barrio", "").strip()
    especie_id = request.GET.get("especie", "").strip()

    qs = Arbol.objects.select_related("especie", "barrio").all()

    if q:
        qs = qs.filter(
			Q(direccion__icontains=q)
			| Q(especie__nombre_comun__icontains=q)
			| Q(barrio__nombre__icontains=q)
		)

    if estado:
        qs = qs.filter(estado=estado)

    if barrio_id.isdigit():
        qs = qs.filter(barrio_id=int(barrio_id))

    if especie_id.isdigit():
        qs = qs.filter(especie_id=int(especie_id))

    qs = qs.order_by("id")

    context = {
		"arboles": qs,
		"q": q,
		"estado": estado,
		"barrio_id": barrio_id,
		"especie_id": especie_id,
		"especies": Especie.objects.order_by("nombre_comun"),
		"barrios": Barrio.objects.order_by("nombre"),
		"estados": Arbol.Estado.choices,
	}

    return render(request, "inventario/arbol_lista.html", context)



def alcorque_lista(request):
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    barrio_id = request.GET.get("barrio", "").strip()

    qs = Alcorque.objects.select_related("barrio").all()

    if q:
        qs = qs.filter(Q(direccion__icontains=q) | Q(barrio__nombre__icontains=q))

    if estado:
        qs = qs.filter(estado=estado)

    if barrio_id.isdigit():
        qs = qs.filter(barrio_id=int(barrio_id))

    qs = qs.order_by("id")

    context = {
		"alcorques": qs,
		"q": q,
		"estado": estado,
		"barrio_id": barrio_id,
		"barrios": Barrio.objects.order_by("nombre"),
		"estados": Alcorque.Estado.choices,
	}

    return render(request, "inventario/alcorque_lista.html", context)



def arbol_detalle(request, pk):
    arbol = get_object_or_404(Arbol.objects.select_related("especie", "barrio"), pk=pk)
    incidencias = []
    if request.user.is_authenticated:
        incidencias = arbol.arbol_inci.select_related("usuario", "admin_resp").order_by("-fecha_reporte")
    return render(request, "inventario/arbol_detalle.html", {"arbol": arbol, "incidencias": incidencias,})


def alcorque_detalle(request, pk):
    alcorque = get_object_or_404(Alcorque.objects.select_related("barrio"), pk=pk)
    incidencias = []
    if request.user.is_authenticated:
        incidencias = alcorque.alcorque_inci.select_related("usuario", "admin_resp").order_by("-fecha_reporte")
    return render(request, "inventario/alcorque_detalle.html", {"alcorque": alcorque, "incidencias": incidencias,})


@login_required
def arbol_crear(request):
    """Crear nuevo árbol - solo administradores (CU15)"""
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden crear árboles")
        return redirect("arbol_lista")
    
    if request.method == "POST":
        form = ArbolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Árbol creado exitosamente")
            return redirect("arbol_lista")
    else:
        form = ArbolForm()
    
    return render(request, "inventario/arbol_form.html", {"form": form, "accion": "Crear"})


@login_required
def arbol_editar(request, pk):
    """Editar árbol existente - solo administradores (CU15)"""
    arbol = get_object_or_404(Arbol, pk=pk)
    
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden editar árboles")
        return redirect("arbol_detalle", pk=pk)
    
    if request.method == "POST":
        form = ArbolForm(request.POST, instance=arbol)
        if form.is_valid():
            form.save()
            messages.success(request, "Árbol actualizado exitosamente")
            return redirect("arbol_detalle", pk=arbol.pk)
    else:
        form = ArbolForm(instance=arbol)
    
    return render(request, "inventario/arbol_form.html", {"form": form, "accion": "Editar", "arbol": arbol})


@login_required
def alcorque_crear(request):
    """Crear nuevo alcorque - solo administradores (CU15)"""
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden crear alcorques")
        return redirect("alcorque_lista")
    
    if request.method == "POST":
        form = AlcorqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Alcorque creado exitosamente")
            return redirect("alcorque_lista")
    else:
        form = AlcorqueForm()
    
    return render(request, "inventario/alcorque_form.html", {"form": form, "accion": "Crear"})


@login_required
def alcorque_editar(request, pk):
    """Editar alcorque existente - solo administradores (CU15 y CU24)"""
    alcorque = get_object_or_404(Alcorque, pk=pk)
    
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden editar alcorques")
        return redirect("alcorque_detalle", pk=pk)
    
    if request.method == "POST":
        form = AlcorqueForm(request.POST, instance=alcorque)
        if form.is_valid():
            form.save()
            messages.success(request, "Alcorque actualizado exitosamente")
            return redirect("alcorque_detalle", pk=alcorque.pk)
    else:
        form = AlcorqueForm(instance=alcorque)
    
    return render(request, "inventario/alcorque_form.html", {"form": form, "accion": "Editar", "alcorque": alcorque})