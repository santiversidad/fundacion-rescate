import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def _send(subject, template, context, to_email):
    """Envía un email HTML usando un template. Silencia errores internamente."""
    try:
        html = render_to_string(template, context)
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html,
            fail_silently=False,
        )
    except Exception as exc:
        logger.warning('Email no enviado [%s] a %s: %s', template, to_email, exc)


def email_inscripcion_evento(inscripcion):
    _send(
        subject=f'Inscripción confirmada: {inscripcion.evento.titulo}',
        template='emails/inscripcion_evento.html',
        context={'inscripcion': inscripcion},
        to_email=inscripcion.usuario.email,
    )


def email_evento_iniciado(evento):
    """Notifica a todos los inscritos que el evento ha comenzado.
    Retorna (enviados, fallidos)."""
    enviados = 0
    fallidos = 0
    for inscripcion in evento.inscripciones.select_related('usuario').all():
        email = inscripcion.usuario.email
        if not email:
            continue
        try:
            html = render_to_string('emails/evento_iniciado.html', {
                'evento': evento,
                'usuario': inscripcion.usuario,
            })
            send_mail(
                subject=f'¡El evento ha comenzado! {evento.titulo}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html,
                fail_silently=False,
            )
            enviados += 1
        except Exception as exc:
            logger.error('Error enviando inicio evento [%s] a %s: %s', evento.titulo, email, exc)
            fallidos += 1
    return enviados, fallidos


def email_evento_cancelado(evento):
    """Notifica la cancelación del evento a todos los inscritos.
    Retorna (enviados, fallidos)."""
    enviados = 0
    fallidos = 0
    for inscripcion in evento.inscripciones.select_related('usuario').all():
        email = inscripcion.usuario.email
        if not email:
            continue
        try:
            html = render_to_string('emails/evento_cancelado.html', {
                'evento': evento,
                'usuario': inscripcion.usuario,
            })
            send_mail(
                subject=f'Evento cancelado: {evento.titulo}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html,
                fail_silently=False,
            )
            enviados += 1
        except Exception as exc:
            logger.error('Error enviando cancelación [%s] a %s: %s', evento.titulo, email, exc)
            fallidos += 1
    return enviados, fallidos
