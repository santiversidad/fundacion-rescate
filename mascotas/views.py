from django.shortcuts import render, get_object_or_404
from .models import Mascota


def catalogo(request):
    mascotas = Mascota.objects.filter(estado='disponible')

    # Filtros
    especie = request.GET.get('especie')
    sexo    = request.GET.get('sexo')

    if especie:
        mascotas = mascotas.filter(especie=especie)
    if sexo:
        mascotas = mascotas.filter(sexo=sexo)

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