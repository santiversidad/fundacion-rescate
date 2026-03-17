from django.shortcuts import render
from .models import MiembroEquipo, ContenidoNosotros
from mascotas.models import Mascota


def inicio(request):
    mascotas_destacadas = Mascota.objects.filter(
        estado='disponible'
    ).order_by('-fecha_ingreso')[:3]

    return render(request, 'institucional/inicio.html', {
        'mascotas_destacadas': mascotas_destacadas,
    })


def nosotros(request):
    contenido = ContenidoNosotros.objects.first()
    equipo = MiembroEquipo.objects.filter(activo=True)

    return render(request, 'institucional/nosotros.html', {
        'contenido': contenido,
        'equipo': equipo,
    })


def contacto(request):
    return render(request, 'institucional/contacto.html')