from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Mascota


def catalogo(request):
    mascotas_lista = Mascota.objects.filter(estado='disponible')

    # Filtros
    especie = request.GET.get('especie')
    sexo    = request.GET.get('sexo')
    q       = request.GET.get('q', '').strip()

    if especie:
        mascotas_lista = mascotas_lista.filter(especie=especie)
    if sexo:
        mascotas_lista = mascotas_lista.filter(sexo=sexo)
    if q:
        mascotas_lista = mascotas_lista.filter(
            Q(nombre__icontains=q) |
            Q(raza__icontains=q) |
            Q(descripcion__icontains=q)
        )

    mascotas_lista = mascotas_lista.prefetch_related('fotos').order_by('-fecha_ingreso')

    # Paginación
    paginador = Paginator(mascotas_lista, 9)
    mascotas = paginador.get_page(request.GET.get('pagina', 1))

    return render(request, 'mascotas/catalogo.html', {
        'mascotas': mascotas,
        'especie_activa': especie or '',
        'sexo_activo': sexo or '',
        'q': q,
    })


def detalle_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'mascotas/detalle.html', {
        'mascota': mascota
    })