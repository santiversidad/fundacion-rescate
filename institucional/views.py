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
from .emails import email_inscripcion_evento
from mascotas.models import Mascota
from config.middleware import rate_limit

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
    proximos    = Evento.objects.filter(estado='proximo').order_by('fecha')
    en_curso    = Evento.objects.filter(estado='en_curso').order_by('fecha')
    finalizados = Evento.objects.filter(estado='finalizado').order_by('-fecha')[:3]

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
@rate_limit(max_requests=20, window_seconds=3600, key_prefix='evento')
def inscribirse_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if evento.esta_lleno():
        messages.warning(request, '⚠️ Lo sentimos, este evento ya no tiene cupos disponibles.')
        return redirect('institucional:detalle_evento', pk=pk)

    if InscripcionEvento.objects.filter(evento=evento, usuario=request.user).exists():
        messages.warning(request, '⚠️ Ya estás inscrito en este evento.')
        return redirect('institucional:detalle_evento', pk=pk)

    inscripcion = InscripcionEvento.objects.create(evento=evento, usuario=request.user)
    email_inscripcion_evento(inscripcion)
    messages.success(request, f'✅ Te inscribiste correctamente en {evento.titulo}.')
    return redirect('institucional:detalle_evento', pk=pk)


def contacto(request):
    return render(request, 'institucional/contacto.html', {
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
    })