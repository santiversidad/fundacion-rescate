from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Mascota


def catalogo(request):
    mascotas_lista = Mascota.objects.filter(estado='disponible')

    # Filtros
    especie = request.GET.get('especie')
    sexo    = request.GET.get('sexo')

    if especie:
        mascotas_lista = mascotas_lista.filter(especie=especie)
    if sexo:
        mascotas_lista = mascotas_lista.filter(sexo=sexo)

    mascotas_lista = mascotas_lista.prefetch_related('fotos').order_by('-fecha_ingreso')

    # Paginación
    paginador = Paginator(mascotas_lista, 9)
    pagina_num = request.GET.get('pagina', 1)
    mascotas = paginador.get_page(pagina_num)

    return render(request, 'mascotas/catalogo.html', {
        'mascotas': mascotas,
        'especie_activa': especie or '',
        'sexo_activo': sexo or '',
    })


def detalle_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'mascotas/detalle.html', {
        'mascota': mascota
    })