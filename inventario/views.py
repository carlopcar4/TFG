from django.views.generic import ListView, DetailView, UpdateView
from .models import Elemento, Especie, Barrio, ESTADO, TIPO, POTENCIAL
from django.shortcuts import redirect,render, get_object_or_404
from .forms import nuevoBarrio, elementoNuevoForm, editarElemForm, nuevaEspecie

# -------------------- ARBOLES ---------------------------------
class Arboles(ListView):
    model = Elemento
    context_object_name = 'arboles'
    template_name = 'inventario/arboles.html'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            arboles = Elemento.objects.all()
        else:
            return redirect('')

        especie = self.request.GET.get('especie')
        barrio = self.request.GET.get('barrio')
        estado = self.request.GET.get('estado')
        direccion = self.request.GET.get('direccion')
        tipo = self.request.GET.get('tipo')

        if especie:
            arboles = arboles.filter(especie__nombre_comun=especie)
        if barrio:
            arboles = arboles.filter(barrio__nombre=barrio)
        if estado:
            arboles = arboles.filter(estado=estado)
        if direccion:
            arboles = arboles.filter(direccion__icontains=direccion)
        if tipo:
            arboles = arboles.filter(tipo=tipo)
        return arboles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especies'] = Especie.objects.all()
        context['barrios'] = Barrio.objects.all()
        context['estados'] = ESTADO
        context['tipos'] = TIPO
        return context

# -------------------- ESPECIES ---------------------------------
class Especies(ListView):
    template_name = 'inventario/especies.html'
    context_object_name = 'especies'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            especies = Especie.objects.all()
        else:
            return render('inicio')
        return especies

# -------------------- NUEVA ESPECIES ---------------------------------
def especieNueva(request):
    if request.method == 'POST':
        form = nuevaEspecie(request.POST)
        if form.is_valid():
            especie = form.save(commit=False)
            especie.save()
            return redirect('especies')
    else:
        form = nuevaEspecie()
    return render(request, 'inventario/especieNueva.html', {'form':form})

# -------------------- BARRIOS ---------------------------------
class Barrios(ListView):
    template_name = 'inventario/barrios.html'
    context_object_name = 'barrios'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            barrios = Barrio.objects.all()
        else:
            return render('inicio')
        return barrios

# -------------------- NUEVO BARRIO ---------------------------------
def barrioNuevo(request):
    if request.method == 'POST':
        form = nuevoBarrio(request.POST)
        if form.is_valid():
            especie = form.save(commit=False)
            especie.save()
            return redirect('barrios')
    else:
        form = nuevoBarrio()
    return render(request, 'inventario/barrioNuevo.html', {'form':form})

# -------------------- DETALLES ARBOL ---------------------------------
class ArbolDetalle(DetailView):
    model = Elemento
    template_name = 'inventario/arbolDetalle.html'

# -------------------- EDITAR ARBOL ---------------------------------
def arbolEditar(request, pk):
    barrios = Barrio.objects.all()
    especies = Especie.objects.all()
    elemento = get_object_or_404(Elemento, pk=pk)
    if request.method == 'POST':
        datos = request.POST.copy()
        if datos.get('latitud'):
                datos['latitud'] = datos['latitud'].replace(',','.')
        if datos.get('longitud'):
            datos['longitud'] = datos['longitud'].replace(',','.')
        form = editarElemForm(datos, instance=elemento)
        if form.is_valid():
            elemento = form.save()
            return redirect('arboles')
    else:
        form = editarElemForm(instance=elemento)
    return render(request, 'inventario/arbolEditar.html',{'form':form, 'elemento':elemento, 'tipo':TIPO, 'barrios':barrios, 'especies':especies,'estados':ESTADO,'potencial':POTENCIAL})

# -------------------- AÑAIDR ARBOL ---------------------------------
def añadirArbol(request):
    barrios = Barrio.objects.all()
    especies = Especie.objects.all()
    if request.method == 'POST':
        form = elementoNuevoForm(request.POST)
        if form.is_valid():
            elemento = form.save(commit=False)
            elemento.save()
            return redirect('arboles')
    else:
        form = elementoNuevoForm()
    return render(request, 'inventario/nuevo.html', {'form':form, 'tipo':TIPO, 'barrios':barrios, 'especies':especies,'estados':ESTADO,'potencial':POTENCIAL})