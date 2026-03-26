from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import (
    MiembroEquipo,
    ContenidoNosotros,
    PreguntaFrecuente,
    Testimonio,
    Evento,
    InscripcionEvento,
)
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
    equipo    = MiembroEquipo.objects.filter(activo=True)

    return render(request, 'institucional/nosotros.html', {
        'contenido': contenido,
        'equipo':    equipo,
    })


def como_ayudar(request):
    return render(request, 'institucional/como_ayudar.html')


def preguntas_frecuentes(request):
    preguntas = PreguntaFrecuente.objects.filter(activa=True)
    return render(request, 'institucional/preguntas_frecuentes.html', {
        'preguntas': preguntas,
    })


def testimonios(request):
    lista = Testimonio.objects.filter(aprobado=True)
    return render(request, 'institucional/testimonios.html', {
        'testimonios': lista,
    })


def eventos(request):
    todos_eventos = Evento.objects.filter(
        estado__in=['proximo', 'en_curso', 'finalizado']
    ).order_by('fecha')

    proximos    = [e for e in todos_eventos if e.estado == 'proximo']
    en_curso    = [e for e in todos_eventos if e.estado == 'en_curso']
    finalizados = [e for e in todos_eventos if e.estado == 'finalizado'][:3]

    return render(request, 'institucional/eventos.html', {
        'proximos':    proximos,
        'en_curso':    en_curso,
        'finalizados': finalizados,
    })


def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    inscrito = False

    if request.user.is_authenticated:
        inscrito = InscripcionEvento.objects.filter(
            evento=evento,
            usuario=request.user
        ).exists()

    return render(request, 'institucional/detalle_evento.html', {
        'evento':   evento,
        'inscrito': inscrito,
    })


@login_required
def inscribirse_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if evento.esta_lleno():
        messages.warning(request, '⚠️ Lo sentimos, este evento ya no tiene cupos disponibles.')
        return redirect('institucional:detalle_evento', pk=pk)

    if InscripcionEvento.objects.filter(evento=evento, usuario=request.user).exists():
        messages.warning(request, '⚠️ Ya estás inscrito en este evento.')
        return redirect('institucional:detalle_evento', pk=pk)

    InscripcionEvento.objects.create(evento=evento, usuario=request.user)
    messages.success(request, f'✅ Te inscribiste correctamente en {evento.titulo}.')
    return redirect('institucional:detalle_evento', pk=pk)


def contacto(request):
    return render(request, 'institucional/contacto.html', {
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
    })