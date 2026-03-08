from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mascotas.models import Mascota
from .models import SolicitudAdopcion


@login_required
def solicitar_adopcion(request, mascota_pk):
    mascota = get_object_or_404(Mascota, pk=mascota_pk, estado='disponible')

    if request.method == 'POST':
        SolicitudAdopcion.objects.create(
            usuario=request.user,
            mascota=mascota,
            motivo=request.POST['motivo'],
            tipo_vivienda=request.POST['tipo_vivienda'],
            tiene_otros_animales='tiene_otros_animales' in request.POST,
        )
        messages.success(request, '✅ Tu solicitud fue enviada correctamente. Te notificaremos cuando sea revisada.')
        return redirect('adopciones:mis_solicitudes')

    return render(request, 'adopciones/solicitar.html', {
        'mascota': mascota
    })


@login_required
def mis_solicitudes(request):
    solicitudes = SolicitudAdopcion.objects.filter(usuario=request.user)
    return render(request, 'adopciones/mis_solicitudes.html', {
        'solicitudes': solicitudes
    })