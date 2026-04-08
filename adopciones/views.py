import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from mascotas.models import Mascota
from .models import SolicitudAdopcion
from .forms import SolicitudAdopcionForm
from .emails import email_solicitud_enviada
from config.middleware import rate_limit

logger = logging.getLogger(__name__)


@login_required
@rate_limit(max_requests=10, window_seconds=3600, key_prefix='adopcion')
def solicitar_adopcion(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk, estado='disponible')

    # Excluir rechazadas Y canceladas para permitir re-solicitar
    solicitud_activa = SolicitudAdopcion.objects.filter(
        usuario=request.user,
        mascota=mascota,
    ).exclude(estado__in=['rechazada', 'cancelada']).first()

    if solicitud_activa:
        messages.warning(
            request,
            f'Ya tienes una solicitud activa ({solicitud_activa.get_estado_display()}) '
            f'para {mascota.nombre}. Puedes consultarla en "Mis solicitudes".'
        )
        return redirect('adopciones:mis_solicitudes')

    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            solicitud = SolicitudAdopcion.objects.create(
                usuario=request.user,
                mascota=mascota,
                # Sección 1
                nombre_completo=cd['nombre_completo'],
                telefono=cd['telefono'],
                ciudad=cd['ciudad'],
                # Sección 2
                tipo_vivienda=cd['tipo_vivienda'],
                vivienda_propia=cd.get('vivienda_propia', False),
                permiso_arrendador=cd.get('permiso_arrendador', False),
                tiene_patio=cd.get('tiene_patio', False),
                patio_cercado=cd.get('patio_cercado', False),
                personas_en_hogar=cd['personas_en_hogar'],
                ninos_en_hogar=cd.get('ninos_en_hogar', False),
                edad_ninos=cd.get('edad_ninos', ''),
                alguien_alergico=cd.get('alguien_alergico', False),
                # Sección 3
                tiene_otros_animales=cd.get('tiene_otros_animales', False),
                descripcion_otros_animales=cd.get('descripcion_otros_animales', ''),
                experiencia_previa=cd.get('experiencia_previa', False),
                que_paso_mascotas_anteriores=cd.get('que_paso_mascotas_anteriores', ''),
                veterinario_referencia=cd.get('veterinario_referencia', ''),
                # Sección 4
                motivo=cd['motivo'],
                horas_fuera_casa=cd['horas_fuera_casa'],
                nivel_actividad=cd['nivel_actividad'],
                viaja_frecuentemente=cd.get('viaja_frecuentemente', False),
                plan_cuidado_viajes=cd.get('plan_cuidado_viajes', ''),
                presupuesto_veterinario=cd['presupuesto_veterinario'],
                # Sección 5
                compromiso_veterinario=cd['compromiso_veterinario'],
                compromiso_no_abandono=cd['compromiso_no_abandono'],
                acepta_seguimiento=cd['acepta_seguimiento'],
                acepta_terminos=cd['acepta_terminos'],
            )
            email_solicitud_enviada(solicitud)
            messages.success(
                request,
                f'Tu solicitud de adopción para {mascota.nombre} fue enviada correctamente. '
                'Nuestro equipo la revisará y te contactará en 3–5 días hábiles.'
            )
            return redirect('adopciones:mis_solicitudes')
    else:
        form = SolicitudAdopcionForm()

    foto_principal = (
        mascota.fotos.filter(es_principal=True).first()
        or mascota.fotos.first()
    )

    return render(request, 'adopciones/solicitar.html', {
        'mascota': mascota,
        'form': form,
        'foto_principal': foto_principal,
    })


@login_required
def mis_solicitudes(request):
    solicitudes = SolicitudAdopcion.objects.filter(
        usuario=request.user
    ).select_related('mascota').order_by('-fecha_solicitud')
    return render(request, 'adopciones/mis_solicitudes.html', {
        'solicitudes': solicitudes,
    })


@login_required
@require_POST
def cancelar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudAdopcion, pk=pk, usuario=request.user)
    if solicitud.estado == 'pendiente':
        solicitud.estado = 'cancelada'
        solicitud.save()
        messages.info(
            request,
            f'Tu solicitud para {solicitud.mascota.nombre} ha sido cancelada.'
        )
    else:
        messages.warning(
            request,
            'Solo puedes cancelar solicitudes que estén en estado pendiente.'
        )
    return redirect('adopciones:mis_solicitudes')