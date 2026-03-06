from django.shortcuts import render, get_object_or_404
from .models import Mascota


def catalogo(request):
    mascotas = Mascota.objects.filter(estado='disponible')
    return render(request, 'mascotas/catalogo.html', {
        'mascotas': mascotas
    })


def detalle_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'mascotas/detalle.html', {
        'mascota': mascota
    })