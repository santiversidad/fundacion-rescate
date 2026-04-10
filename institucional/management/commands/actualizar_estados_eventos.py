"""
Management command: actualizar_estados_eventos
Cambia 'proximo' → 'en_curso' para eventos cuya fecha ya llegó
y notifica por correo a los inscritos.

Uso:
    python manage.py actualizar_estados_eventos
    # Agregar al cron/scheduler:
    # */5 * * * * cd /app && python manage.py actualizar_estados_eventos
"""
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from institucional.models import Evento
from institucional.emails import email_evento_iniciado

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Cambia eventos próximos a en_curso cuando su fecha ha llegado y notifica a los inscritos.'

    def handle(self, *args, **options):
        ahora = timezone.now()
        eventos_a_iniciar = Evento.objects.filter(
            estado='proximo',
            fecha__lte=ahora,
        )

        total = eventos_a_iniciar.count()
        if total == 0:
            self.stdout.write('Sin eventos para actualizar.')
            return

        for evento in eventos_a_iniciar:
            evento.estado = 'en_curso'
            evento.save(update_fields=['estado'])

            enviados, fallidos = email_evento_iniciado(evento)
            self.stdout.write(
                f'[OK] "{evento.titulo}" → en_curso | '
                f'Notificaciones: {enviados} enviadas, {fallidos} fallidas.'
            )
            logger.info(
                'Evento "%s" (pk=%s) cambiado a en_curso. Emails: %s enviados, %s fallidos.',
                evento.titulo, evento.pk, enviados, fallidos,
            )

        self.stdout.write(self.style.SUCCESS(f'{total} evento(s) actualizados.'))