from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Arbol, Alcorque

def arbol_lista(request):
	q = request.GET.get("q", "").strip()
	estado = request.GET.get("estado", "").strip()
	barrio_id = request.GET.get("barrio", "").strip()

	qs = Arbol.objects.select_related("especie", "barrio").all()

# Buscar por dirección
	if q:
			qs = qs.filter(Q(direccion__icontains=q) | Q(especie__nombre_comun__icontains=q) | Q(barrio__nombre__icontains=q))

	if estado:
		qs = qs.filter(estado=estado)

	if barrio_id.isdigit():
		qs = qs.filter(barrio_id=int(barrio_id))

	qs = qs.order_by("id")

	context = {
		"arboles": qs,
		"q": q,
		"estado": estado,
		"barrio_id": barrio_id,
	}

	return render(request, "inventario/arbol_lista.html", context)


def alcorque_lista(request):
	q = request.GET.get("q", "").strip()
	estado = request.GET.get("estado", "").strip()
	barrio_id = request.GET.get("barrio", "").strip()

	qs = Alcorque.objects.select_related("barrio").all()

# Buscar por dirección
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
	}

	return render(request, "inventario/alcorque_lista.html", context)


def arbol_detalle(request, pk):
	arbol = get_object_or_404(
		Arbol.objects.select_related("especie", "barrio"),
		pk=pk
	)
	return render(request, "inventario/arbol_detalle.html", {"arbol": arbol})


def alcorque_detalle(request, pk):
	alcorque = get_object_or_404(
		Alcorque.objects.select_related("barrio"),
		pk=pk
	)
	return render(request, "inventario/alcorque_detalle.html", {"alcorque": alcorque})




