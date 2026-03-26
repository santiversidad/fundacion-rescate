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


def email_solicitud_enviada(solicitud):
    _send(
        subject='Tu solicitud de adopción fue recibida',
        template='emails/adopcion_enviada.html',
        context={'solicitud': solicitud},
        to_email=solicitud.usuario.email,
    )


def email_solicitud_aprobada(solicitud):
    _send(
        subject='¡Tu solicitud de adopción fue aprobada!',
        template='emails/adopcion_aprobada.html',
        context={'solicitud': solicitud},
        to_email=solicitud.usuario.email,
    )


def email_solicitud_rechazada(solicitud):
    _send(
        subject='Actualización sobre tu solicitud de adopción',
        template='emails/adopcion_rechazada.html',
        context={'solicitud': solicitud},
        to_email=solicitud.usuario.email,
    )