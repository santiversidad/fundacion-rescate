from institucional.models import MensajeContacto


def mensajes_no_leidos(request):
    """Inyecta el conteo de mensajes no leídos en todos los templates del dashboard."""
    if request.user.is_authenticated and request.user.is_staff:
        count = MensajeContacto.objects.filter(leido=False).count()
        return {'mensajes_no_leidos': count}
    return {'mensajes_no_leidos': 0}