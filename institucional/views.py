from django.shortcuts import render
from .models import MiembroEquipo, ContenidoNosotros


def inicio(request):
    return render(request, 'institucional/inicio.html')


def nosotros(request):
    contenido = ContenidoNosotros.objects.first()
    equipo = MiembroEquipo.objects.filter(activo=True)

    return render(request, 'institucional/nosotros.html', {
        'contenido': contenido,
        'equipo': equipo,
    })


def contacto(request):
    return render(request, 'institucional/contacto.html')