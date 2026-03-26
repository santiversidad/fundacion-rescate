import time
import logging
from django.core.cache import cache
from django.http import HttpResponse
from functools import wraps

logger = logging.getLogger(__name__)


def rate_limit(max_requests=10, window_seconds=60, key_prefix='rl'):
    """
    Decorator to rate-limit views.
    Uses Django's cache to track request counts per IP.

    Usage:
        @rate_limit(max_requests=5, window_seconds=60)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            ip = _get_client_ip(request)
            cache_key = f'{key_prefix}:{view_func.__name__}:{ip}'

            request_data = cache.get(cache_key)

            if request_data is None:
                cache.set(cache_key, {'count': 1, 'start': time.time()}, window_seconds)
            else:
                elapsed = time.time() - request_data['start']
                if elapsed < window_seconds:
                    if request_data['count'] >= max_requests:
                        logger.warning(
                            'Rate limit exceeded for IP %s on view %s',
                            ip, view_func.__name__
                        )
                        return HttpResponse(
                            '<h1>Demasiadas solicitudes</h1>'
                            '<p>Has realizado demasiadas solicitudes. '
                            'Por favor espera unos minutos antes de intentar de nuevo.</p>',
                            status=429,
                            content_type='text/html; charset=utf-8',
                        )
                    request_data['count'] += 1
                    cache.set(cache_key, request_data, window_seconds)
                else:
                    cache.set(cache_key, {'count': 1, 'start': time.time()}, window_seconds)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def _get_client_ip(request):
    """Get client IP, considering proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')