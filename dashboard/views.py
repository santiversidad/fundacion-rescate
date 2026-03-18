from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .decorators import admin_requerido
from mascotas.models import Mascota, FotoMascota
from adopciones.models import SolicitudAdopcion
from donaciones.models import Donacion
from institucional.models import (
    Evento, MiembroEquipo, Testimonio,
    PreguntaFrecuente, ContenidoNosotros,
    InscripcionEvento
)


@admin_requerido
def inicio(request):
    stats = {
        'total_mascotas':    Mascota.objects.filter(estado='disponible').count(),
        'total_adopciones':  SolicitudAdopcion.objects.filter(estado='aprobada').count(),
        'solicitudes_pendientes': SolicitudAdopcion.objects.filter(estado='pendiente').count(),
        'donaciones_pendientes':  Donacion.objects.filter(estado='pendiente').count(),
        'total_donaciones':  Donacion.objects.filter(estado='verificada').count(),
        'total_eventos':     Evento.objects.filter(estado='proximo').count(),
    }
    solicitudes_recientes = SolicitudAdopcion.objects.order_by('-fecha_solicitud')[:5]
    donaciones_recientes  = Donacion.objects.order_by('-fecha_registro')[:5]

    return render(request, 'dashboard/inicio.html', {
        'stats': stats,
        'solicitudes_recientes': solicitudes_recientes,
        'donaciones_recientes':  donaciones_recientes,
    })


@admin_requerido
def mascotas(request):
    lista = Mascota.objects.all().order_by('-fecha_ingreso')
    return render(request, 'dashboard/mascotas.html', {'mascotas': lista})


@admin_requerido
def agregar_mascota(request):
    if request.method == 'POST':
        mascota = Mascota.objects.create(
            nombre       = request.POST['nombre'],
            especie      = request.POST['especie'],
            raza         = request.POST.get('raza', ''),
            edad_anios   = request.POST['edad_anios'],
            sexo         = request.POST['sexo'],
            descripcion  = request.POST.get('descripcion', ''),
            fecha_ingreso = request.POST['fecha_ingreso'],
            esterilizado = 'esterilizado' in request.POST,
            vacunado     = 'vacunado' in request.POST,
        )
        fotos = request.FILES.getlist('fotos')
        for foto in fotos:
            FotoMascota.objects.create(mascota=mascota, foto=foto)

        messages.success(request, f'✅ {mascota.nombre} fue agregada correctamente.')
        return redirect('dashboard:mascotas')

    return render(request, 'dashboard/agregar_mascota.html')


@admin_requerido
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        mascota.nombre        = request.POST['nombre']
        mascota.especie       = request.POST['especie']
        mascota.raza          = request.POST.get('raza', '')
        mascota.edad_anios    = request.POST['edad_anios']
        mascota.sexo          = request.POST['sexo']
        mascota.descripcion   = request.POST.get('descripcion', '')
        mascota.fecha_ingreso = request.POST['fecha_ingreso']
        mascota.esterilizado  = 'esterilizado' in request.POST
        mascota.vacunado      = 'vacunado' in request.POST
        mascota.estado        = request.POST['estado']
        mascota.save()

        fotos = request.FILES.getlist('fotos')
        for foto in fotos:
            FotoMascota.objects.create(mascota=mascota, foto=foto)

        messages.success(request, f'✅ {mascota.nombre} fue actualizada correctamente.')
        return redirect('dashboard:mascotas')

    return render(request, 'dashboard/editar_mascota.html', {'mascota': mascota})


@admin_requerido
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'✅ {nombre} fue eliminada correctamente.')
        return redirect('dashboard:mascotas')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': mascota})


@admin_requerido
def adopciones(request):
    lista = SolicitudAdopcion.objects.all().order_by('-fecha_solicitud')
    return render(request, 'dashboard/adopciones.html', {'solicitudes': lista})


@admin_requerido
def detalle_adopcion(request, pk):
    solicitud = get_object_or_404(SolicitudAdopcion, pk=pk)

    if request.method == 'POST':
        solicitud.estado = request.POST['estado']
        solicitud.observaciones_admin = request.POST.get('observaciones_admin', '')
        solicitud.save()
        messages.success(request, '✅ Solicitud actualizada correctamente.')
        return redirect('dashboard:adopciones')

    return render(request, 'dashboard/detalle_adopcion.html', {'solicitud': solicitud})


@admin_requerido
def donaciones(request):
    lista = Donacion.objects.all().order_by('-fecha_registro')
    return render(request, 'dashboard/donaciones.html', {'donaciones': lista})


@admin_requerido
def detalle_donacion(request, pk):
    donacion = get_object_or_404(Donacion, pk=pk)

    if request.method == 'POST':
        donacion.estado = request.POST['estado']
        donacion.observaciones = request.POST.get('observaciones', '')
        donacion.save()
        messages.success(request, '✅ Donación actualizada correctamente.')
        return redirect('dashboard:donaciones')

    return render(request, 'dashboard/detalle_donacion.html', {'donacion': donacion})


@admin_requerido
def eventos(request):
    lista = Evento.objects.all().order_by('fecha')
    return render(request, 'dashboard/eventos.html', {'eventos': lista})


@admin_requerido
def agregar_evento(request):
    if request.method == 'POST':
        Evento.objects.create(
            titulo      = request.POST['titulo'],
            descripcion = request.POST['descripcion'],
            fecha       = request.POST['fecha'],
            lugar       = request.POST['lugar'],
            capacidad   = request.POST['capacidad'],
            imagen      = request.FILES.get('imagen'),
        )
        messages.success(request, '✅ Evento creado correctamente.')
        return redirect('dashboard:eventos')
    return render(request, 'dashboard/agregar_evento.html')


@admin_requerido
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        evento.titulo      = request.POST['titulo']
        evento.descripcion = request.POST['descripcion']
        evento.fecha       = request.POST['fecha']
        evento.lugar       = request.POST['lugar']
        evento.capacidad   = request.POST['capacidad']
        evento.estado      = request.POST['estado']
        if request.FILES.get('imagen'):
            evento.imagen  = request.FILES['imagen']
        evento.save()
        messages.success(request, '✅ Evento actualizado correctamente.')
        return redirect('dashboard:eventos')

    return render(request, 'dashboard/editar_evento.html', {'evento': evento})


@admin_requerido
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        titulo = evento.titulo
        evento.delete()
        messages.success(request, f'✅ {titulo} fue eliminado correctamente.')
        return redirect('dashboard:eventos')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': evento})


@admin_requerido
def equipo(request):
    lista = MiembroEquipo.objects.all().order_by('orden')
    return render(request, 'dashboard/equipo.html', {'equipo': lista})


@admin_requerido
def agregar_miembro(request):
    if request.method == 'POST':
        MiembroEquipo.objects.create(
            nombre      = request.POST['nombre'],
            cargo       = request.POST['cargo'],
            descripcion = request.POST.get('descripcion', ''),
            orden       = request.POST.get('orden', 0),
            foto        = request.FILES.get('foto'),
        )
        messages.success(request, '✅ Miembro agregado correctamente.')
        return redirect('dashboard:equipo')
    return render(request, 'dashboard/agregar_miembro.html')


@admin_requerido
def editar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)

    if request.method == 'POST':
        miembro.nombre      = request.POST['nombre']
        miembro.cargo       = request.POST['cargo']
        miembro.descripcion = request.POST.get('descripcion', '')
        miembro.orden       = request.POST.get('orden', 0)
        miembro.activo      = 'activo' in request.POST
        if request.FILES.get('foto'):
            miembro.foto    = request.FILES['foto']
        miembro.save()
        messages.success(request, '✅ Miembro actualizado correctamente.')
        return redirect('dashboard:equipo')

    return render(request, 'dashboard/editar_miembro.html', {'miembro': miembro})


@admin_requerido
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)
    if request.method == 'POST':
        nombre = miembro.nombre
        miembro.delete()
        messages.success(request, f'✅ {nombre} fue eliminado correctamente.')
        return redirect('dashboard:equipo')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': miembro})


@admin_requerido
def testimonios(request):
    lista = Testimonio.objects.all().order_by('-fecha')
    return render(request, 'dashboard/testimonios.html', {'testimonios': lista})


@admin_requerido
def aprobar_testimonio(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    testimonio.aprobado = True
    testimonio.save()
    messages.success(request, '✅ Testimonio aprobado.')
    return redirect('dashboard:testimonios')


@admin_requerido
def rechazar_testimonio(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    testimonio.aprobado = False
    testimonio.save()
    messages.success(request, '✅ Testimonio rechazado.')
    return redirect('dashboard:testimonios')


@admin_requerido
def faq(request):
    lista = PreguntaFrecuente.objects.all().order_by('orden')
    return render(request, 'dashboard/faq.html', {'preguntas': lista})


@admin_requerido
def agregar_faq(request):
    if request.method == 'POST':
        PreguntaFrecuente.objects.create(
            pregunta  = request.POST['pregunta'],
            respuesta = request.POST['respuesta'],
            orden     = request.POST.get('orden', 0),
        )
        messages.success(request, '✅ Pregunta agregada correctamente.')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/agregar_faq.html')


@admin_requerido
def editar_faq(request, pk):
    pregunta = get_object_or_404(PreguntaFrecuente, pk=pk)

    if request.method == 'POST':
        pregunta.pregunta  = request.POST['pregunta']
        pregunta.respuesta = request.POST['respuesta']
        pregunta.orden     = request.POST.get('orden', 0)
        pregunta.activa    = 'activa' in request.POST
        pregunta.save()
        messages.success(request, '✅ Pregunta actualizada correctamente.')
        return redirect('dashboard:faq')

    return render(request, 'dashboard/editar_faq.html', {'pregunta': pregunta})


@admin_requerido
def eliminar_faq(request, pk):
    pregunta = get_object_or_404(PreguntaFrecuente, pk=pk)
    if request.method == 'POST':
        pregunta.delete()
        messages.success(request, '✅ Pregunta eliminada correctamente.')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': pregunta})


@admin_requerido
def contenido_institucional(request):
    contenido = ContenidoNosotros.objects.first()

    if request.method == 'POST':
        if contenido:
            contenido.mision = request.POST['mision']
            contenido.vision = request.POST['vision']
            if request.FILES.get('imagen_mision'):
                contenido.imagen_mision = request.FILES['imagen_mision']
            if request.FILES.get('imagen_vision'):
                contenido.imagen_vision = request.FILES['imagen_vision']
            contenido.save()
        else:
            ContenidoNosotros.objects.create(
                mision        = request.POST['mision'],
                vision        = request.POST['vision'],
                imagen_mision = request.FILES.get('imagen_mision'),
                imagen_vision = request.FILES.get('imagen_vision'),
            )
        messages.success(request, '✅ Contenido institucional actualizado correctamente.')
        return redirect('dashboard:contenido_institucional')

    return render(request, 'dashboard/contenido_institucional.html', {
        'contenido': contenido,
    })