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


def email_donacion_registrada(donacion):
    _send(
        subject='Tu donación fue registrada correctamente',
        template='emails/donacion_registrada.html',
        context={'donacion': donacion},
        to_email=donacion.usuario.email,
    )


def email_donacion_verificada(donacion):
    _send(
        subject='Tu donación fue verificada — ¡Gracias!',
        template='emails/donacion_verificada.html',
        context={'donacion': donacion},
        to_email=donacion.usuario.email,
    )


def email_donacion_rechazada(donacion):
    _send(
        subject='Información sobre tu donación registrada',
        template='emails/donacion_rechazada.html',
        context={'donacion': donacion},
        to_email=donacion.usuario.email,
    )