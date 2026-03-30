from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .decorators import admin_requerido
from .models import RegistroActividad
from mascotas.models import Mascota, FotoMascota
from adopciones.models import SolicitudAdopcion
from adopciones.emails import email_solicitud_aprobada, email_solicitud_rechazada
from donaciones.models import Donacion
from donaciones.emails import email_donacion_verificada, email_donacion_rechazada
from institucional.models import (
    Evento, MiembroEquipo, Testimonio,
    PreguntaFrecuente, ContenidoNosotros,
    InscripcionEvento, MensajeContacto,
)
from .forms import (
    MascotaForm, EventoForm, MiembroEquipoForm,
    PreguntaFrecuenteForm, ContenidoNosotrosForm,
    AdopcionEstadoForm, DonacionEstadoForm,
)


def _registrar_actividad(usuario, accion, modelo, objeto_id, descripcion):
    RegistroActividad.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        descripcion=descripcion,
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
    solicitudes_recientes = SolicitudAdopcion.objects.select_related('usuario', 'mascota').order_by('-fecha_solicitud')[:5]
    donaciones_recientes  = Donacion.objects.select_related('usuario').order_by('-fecha_registro')[:5]
    actividad_reciente = RegistroActividad.objects.select_related('usuario').order_by('-fecha')[:10]

    return render(request, 'dashboard/inicio.html', {
        'stats': stats,
        'solicitudes_recientes': solicitudes_recientes,
        'donaciones_recientes':  donaciones_recientes,
        'actividad_reciente': actividad_reciente,
    })


@admin_requerido
def mascotas(request):
    lista = Mascota.objects.all().order_by('-fecha_ingreso')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/mascotas.html', {'mascotas': pagina})


@admin_requerido
def agregar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = Mascota.objects.create(
                nombre=form.cleaned_data['nombre'],
                especie=form.cleaned_data['especie'],
                raza=form.cleaned_data.get('raza', ''),
                edad_anios=form.cleaned_data['edad_anios'],
                sexo=form.cleaned_data['sexo'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                fecha_ingreso=form.cleaned_data['fecha_ingreso'],
                esterilizado=form.cleaned_data['esterilizado'],
                vacunado=form.cleaned_data['vacunado'],
            )
            fotos = request.FILES.getlist('fotos')
            for foto in fotos:
                FotoMascota.objects.create(mascota=mascota, foto=foto)
            _registrar_actividad(request.user, 'crear', 'Mascota', mascota.pk, f'Mascota agregada: {mascota.nombre}')
            messages.success(request, f'✅ {mascota.nombre} fue agregada correctamente.')
            return redirect('dashboard:mascotas')
    else:
        form = MascotaForm()
    return render(request, 'dashboard/agregar_mascota.html', {'form': form})


@admin_requerido
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota.nombre        = form.cleaned_data['nombre']
            mascota.especie       = form.cleaned_data['especie']
            mascota.raza          = form.cleaned_data.get('raza', '')
            mascota.edad_anios    = form.cleaned_data['edad_anios']
            mascota.sexo          = form.cleaned_data['sexo']
            mascota.descripcion   = form.cleaned_data.get('descripcion', '')
            mascota.fecha_ingreso = form.cleaned_data['fecha_ingreso']
            mascota.esterilizado  = form.cleaned_data['esterilizado']
            mascota.vacunado      = form.cleaned_data['vacunado']
            mascota.estado        = form.cleaned_data['estado']
            mascota.save()

            fotos = request.FILES.getlist('fotos')
            for foto in fotos:
                FotoMascota.objects.create(mascota=mascota, foto=foto)

            _registrar_actividad(request.user, 'editar', 'Mascota', mascota.pk, f'Mascota editada: {mascota.nombre}')
            messages.success(request, f'✅ {mascota.nombre} fue actualizada correctamente.')
            return redirect('dashboard:mascotas')
    else:
        form = MascotaForm()

    return render(request, 'dashboard/editar_mascota.html', {'mascota': mascota, 'form': form})


@admin_requerido
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        _registrar_actividad(request.user, 'eliminar', 'Mascota', None, f'Mascota eliminada: {nombre}')
        messages.success(request, f'✅ {nombre} fue eliminada correctamente.')
        return redirect('dashboard:mascotas')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': mascota})


@admin_requerido
def adopciones(request):
    lista = SolicitudAdopcion.objects.select_related('usuario', 'mascota').order_by('-fecha_solicitud')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/adopciones.html', {'solicitudes': pagina})


@admin_requerido
def detalle_adopcion(request, pk):
    solicitud = get_object_or_404(SolicitudAdopcion, pk=pk)

    if request.method == 'POST':
        form = AdopcionEstadoForm(request.POST)
        if form.is_valid():
            solicitud.estado = form.cleaned_data['estado']
            solicitud.observaciones_admin = form.cleaned_data.get('observaciones_admin', '')
            solicitud.save()
            _registrar_actividad(request.user, 'editar', 'SolicitudAdopcion', solicitud.pk, f'Solicitud actualizada a {solicitud.get_estado_display()}')
            if solicitud.estado == 'aprobada':
                email_solicitud_aprobada(solicitud)
            elif solicitud.estado == 'rechazada':
                email_solicitud_rechazada(solicitud)
            messages.success(request, '✅ Solicitud actualizada correctamente.')
            return redirect('dashboard:adopciones')
    else:
        form = AdopcionEstadoForm()

    return render(request, 'dashboard/detalle_adopcion.html', {'solicitud': solicitud, 'form': form})


@admin_requerido
def donaciones(request):
    lista = Donacion.objects.select_related('usuario').order_by('-fecha_registro')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/donaciones.html', {'donaciones': pagina})


@admin_requerido
def detalle_donacion(request, pk):
    donacion = get_object_or_404(Donacion, pk=pk)

    if request.method == 'POST':
        form = DonacionEstadoForm(request.POST)
        if form.is_valid():
            donacion.estado = form.cleaned_data['estado']
            donacion.observaciones = form.cleaned_data.get('observaciones', '')
            donacion.save()
            _registrar_actividad(request.user, 'verificar', 'Donacion', donacion.pk, f'Donación actualizada a {donacion.get_estado_display()}')
            if donacion.estado == 'verificada':
                email_donacion_verificada(donacion)
            elif donacion.estado == 'rechazada':
                email_donacion_rechazada(donacion)
            messages.success(request, '✅ Donación actualizada correctamente.')
            return redirect('dashboard:donaciones')
    else:
        form = DonacionEstadoForm()

    return render(request, 'dashboard/detalle_donacion.html', {'donacion': donacion, 'form': form})


@admin_requerido
def eventos(request):
    lista = Evento.objects.all().order_by('fecha')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/eventos.html', {'eventos': pagina})


@admin_requerido
def agregar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = Evento.objects.create(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                fecha=form.cleaned_data['fecha'],
                lugar=form.cleaned_data['lugar'],
                capacidad=form.cleaned_data['capacidad'],
                imagen=form.cleaned_data.get('imagen'),
            )
            _registrar_actividad(request.user, 'crear', 'Evento', evento.pk, f'Evento creado: {evento.titulo}')
            messages.success(request, '✅ Evento creado correctamente.')
            return redirect('dashboard:eventos')
    else:
        form = EventoForm()
    return render(request, 'dashboard/agregar_evento.html', {'form': form})


@admin_requerido
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento.titulo      = form.cleaned_data['titulo']
            evento.descripcion = form.cleaned_data['descripcion']
            evento.fecha       = form.cleaned_data['fecha']
            evento.lugar       = form.cleaned_data['lugar']
            evento.capacidad   = form.cleaned_data['capacidad']
            evento.estado      = form.cleaned_data['estado']
            if form.cleaned_data.get('imagen'):
                evento.imagen  = form.cleaned_data['imagen']
            evento.save()
            _registrar_actividad(request.user, 'editar', 'Evento', evento.pk, f'Evento editado: {evento.titulo}')
            messages.success(request, '✅ Evento actualizado correctamente.')
            return redirect('dashboard:eventos')
    else:
        form = EventoForm()

    return render(request, 'dashboard/editar_evento.html', {'evento': evento, 'form': form})


@admin_requerido
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        titulo = evento.titulo
        evento.delete()
        _registrar_actividad(request.user, 'eliminar', 'Evento', None, f'Evento eliminado: {titulo}')
        messages.success(request, f'✅ {titulo} fue eliminado correctamente.')
        return redirect('dashboard:eventos')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': evento})


@admin_requerido
def equipo(request):
    lista = MiembroEquipo.objects.all().order_by('orden')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/equipo.html', {'equipo': pagina})


@admin_requerido
def agregar_miembro(request):
    if request.method == 'POST':
        form = MiembroEquipoForm(request.POST, request.FILES)
        if form.is_valid():
            miembro = MiembroEquipo.objects.create(
                nombre=form.cleaned_data['nombre'],
                cargo=form.cleaned_data['cargo'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                orden=form.cleaned_data.get('orden') or 0,
                foto=form.cleaned_data.get('foto'),
            )
            _registrar_actividad(request.user, 'crear', 'MiembroEquipo', miembro.pk, f'Miembro agregado: {miembro.nombre}')
            messages.success(request, '✅ Miembro agregado correctamente.')
            return redirect('dashboard:equipo')
    else:
        form = MiembroEquipoForm()
    return render(request, 'dashboard/agregar_miembro.html', {'form': form})


@admin_requerido
def editar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)

    if request.method == 'POST':
        form = MiembroEquipoForm(request.POST, request.FILES)
        if form.is_valid():
            miembro.nombre      = form.cleaned_data['nombre']
            miembro.cargo       = form.cleaned_data['cargo']
            miembro.descripcion = form.cleaned_data.get('descripcion', '')
            miembro.orden       = form.cleaned_data.get('orden') or 0
            miembro.activo      = form.cleaned_data['activo']
            if form.cleaned_data.get('foto'):
                miembro.foto    = form.cleaned_data['foto']
            miembro.save()
            _registrar_actividad(request.user, 'editar', 'MiembroEquipo', miembro.pk, f'Miembro editado: {miembro.nombre}')
            messages.success(request, '✅ Miembro actualizado correctamente.')
            return redirect('dashboard:equipo')
    else:
        form = MiembroEquipoForm()

    return render(request, 'dashboard/editar_miembro.html', {'miembro': miembro, 'form': form})


@admin_requerido
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)
    if request.method == 'POST':
        nombre = miembro.nombre
        miembro.delete()
        _registrar_actividad(request.user, 'eliminar', 'MiembroEquipo', None, f'Miembro eliminado: {nombre}')
        messages.success(request, f'✅ {nombre} fue eliminado correctamente.')
        return redirect('dashboard:equipo')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': miembro})


@admin_requerido
def testimonios(request):
    lista = Testimonio.objects.all().order_by('-fecha')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/testimonios.html', {'testimonios': pagina})


@admin_requerido
@require_POST
def aprobar_testimonio(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    testimonio.aprobado = True
    testimonio.save()
    _registrar_actividad(request.user, 'aprobar', 'Testimonio', testimonio.pk, f'Testimonio aprobado: {testimonio.nombre}')
    messages.success(request, '✅ Testimonio aprobado.')
    return redirect('dashboard:testimonios')


@admin_requerido
@require_POST
def rechazar_testimonio(request, pk):
    testimonio = get_object_or_404(Testimonio, pk=pk)
    testimonio.aprobado = False
    testimonio.save()
    _registrar_actividad(request.user, 'rechazar', 'Testimonio', testimonio.pk, f'Testimonio rechazado: {testimonio.nombre}')
    messages.success(request, '✅ Testimonio rechazado.')
    return redirect('dashboard:testimonios')


@admin_requerido
def faq(request):
    lista = PreguntaFrecuente.objects.all().order_by('orden')
    paginador = Paginator(lista, 15)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/faq.html', {'preguntas': pagina})


@admin_requerido
def agregar_faq(request):
    if request.method == 'POST':
        form = PreguntaFrecuenteForm(request.POST)
        if form.is_valid():
            pregunta = PreguntaFrecuente.objects.create(
                pregunta=form.cleaned_data['pregunta'],
                respuesta=form.cleaned_data['respuesta'],
                orden=form.cleaned_data.get('orden') or 0,
            )
            _registrar_actividad(request.user, 'crear', 'PreguntaFrecuente', pregunta.pk, f'Pregunta agregada: {pregunta.pregunta[:50]}')
            messages.success(request, '✅ Pregunta agregada correctamente.')
            return redirect('dashboard:faq')
    else:
        form = PreguntaFrecuenteForm()
    return render(request, 'dashboard/agregar_faq.html', {'form': form})


@admin_requerido
def editar_faq(request, pk):
    pregunta = get_object_or_404(PreguntaFrecuente, pk=pk)

    if request.method == 'POST':
        form = PreguntaFrecuenteForm(request.POST)
        if form.is_valid():
            pregunta.pregunta  = form.cleaned_data['pregunta']
            pregunta.respuesta = form.cleaned_data['respuesta']
            pregunta.orden     = form.cleaned_data.get('orden') or 0
            pregunta.activa    = form.cleaned_data['activa']
            pregunta.save()
            _registrar_actividad(request.user, 'editar', 'PreguntaFrecuente', pregunta.pk, f'Pregunta editada: {pregunta.pregunta[:50]}')
            messages.success(request, '✅ Pregunta actualizada correctamente.')
            return redirect('dashboard:faq')
    else:
        form = PreguntaFrecuenteForm()

    return render(request, 'dashboard/editar_faq.html', {'pregunta': pregunta, 'form': form})


@admin_requerido
def eliminar_faq(request, pk):
    pregunta = get_object_or_404(PreguntaFrecuente, pk=pk)
    if request.method == 'POST':
        texto = pregunta.pregunta[:50]
        pregunta.delete()
        _registrar_actividad(request.user, 'eliminar', 'PreguntaFrecuente', None, f'Pregunta eliminada: {texto}')
        messages.success(request, '✅ Pregunta eliminada correctamente.')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/confirmar_eliminar.html', {'objeto': pregunta})


@admin_requerido
def contenido_institucional(request):
    contenido = ContenidoNosotros.objects.first()

    if request.method == 'POST':
        form = ContenidoNosotrosForm(request.POST, request.FILES)
        if form.is_valid():
            if contenido:
                contenido.mision = form.cleaned_data['mision']
                contenido.vision = form.cleaned_data['vision']
                if form.cleaned_data.get('imagen_mision'):
                    contenido.imagen_mision = form.cleaned_data['imagen_mision']
                if form.cleaned_data.get('imagen_vision'):
                    contenido.imagen_vision = form.cleaned_data['imagen_vision']
                contenido.save()
                _registrar_actividad(request.user, 'editar', 'ContenidoNosotros', contenido.pk, 'Contenido institucional actualizado')
            else:
                contenido = ContenidoNosotros.objects.create(
                    mision=form.cleaned_data['mision'],
                    vision=form.cleaned_data['vision'],
                    imagen_mision=form.cleaned_data.get('imagen_mision'),
                    imagen_vision=form.cleaned_data.get('imagen_vision'),
                )
                _registrar_actividad(request.user, 'crear', 'ContenidoNosotros', contenido.pk, 'Contenido institucional creado')
            messages.success(request, '✅ Contenido institucional actualizado correctamente.')
            return redirect('dashboard:contenido_institucional')
    else:
        form = ContenidoNosotrosForm()

    return render(request, 'dashboard/contenido_institucional.html', {
        'contenido': contenido,
        'form': form,
    })


@admin_requerido
def mensajes(request):
    lista = MensajeContacto.objects.all()
    paginador = Paginator(lista, 20)
    pagina = paginador.get_page(request.GET.get('pagina', 1))
    return render(request, 'dashboard/mensajes.html', {'mensajes': pagina})


@admin_requerido
def marcar_mensaje_leido(request, pk):
    mensaje = MensajeContacto.objects.get(pk=pk)
    mensaje.leido = True
    mensaje.save()
    return render(request, 'dashboard/detalle_mensaje.html', {'mensaje': mensaje})