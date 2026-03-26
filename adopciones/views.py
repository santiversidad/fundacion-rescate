from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mascotas.models import Mascota
from .models import SolicitudAdopcion
from .forms import SolicitudAdopcionForm
from config.middleware import rate_limit


@login_required
@rate_limit(max_requests=10, window_seconds=3600, key_prefix='adopcion')
def solicitar_adopcion(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk, estado='disponible')

    solicitud_activa = SolicitudAdopcion.objects.filter(
        usuario=request.user,
        mascota=mascota,
    ).exclude(estado='rechazada').first()

    if solicitud_activa:
        messages.warning(
            request,
            f'⚠️ Ya tienes una solicitud {solicitud_activa.get_estado_display()} '
            f'para {mascota.nombre}. No puedes enviar otra hasta que sea resuelta.'
        )
        return redirect('adopciones:mis_solicitudes')

    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            SolicitudAdopcion.objects.create(
                usuario=request.user,
                mascota=mascota,
                motivo=form.cleaned_data['motivo'],
                tipo_vivienda=form.cleaned_data['tipo_vivienda'],
                tiene_otros_animales=form.cleaned_data['tiene_otros_animales'],
            )
            messages.success(
                request,
                '✅ Tu solicitud fue enviada correctamente. Te notificaremos cuando sea revisada.'
            )
            return redirect('adopciones:mis_solicitudes')
    else:
        form = SolicitudAdopcionForm()

    return render(request, 'adopciones/solicitar.html', {
        'mascota': mascota,
        'form': form,
    })


@login_required
def mis_solicitudes(request):
    solicitudes = SolicitudAdopcion.objects.filter(
        usuario=request.user
    ).select_related('mascota').order_by('-fecha_solicitud')
    return render(request, 'adopciones/mis_solicitudes.html', {
        'solicitudes': solicitudes
    })
