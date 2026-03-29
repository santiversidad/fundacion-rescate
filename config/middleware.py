import time
import logging
from django.core.cache import cache
from django.http import HttpResponse
from functools import wraps

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """Agrega headers de seguridad adicionales a todas las respuestas."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        response['X-Permitted-Cross-Domain-Policies'] = 'none'
        return response


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
                        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demasiadas solicitudes — Fundación Rescate Animal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
        .card { border: none; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
    </style>
</head>
<body class="d-flex align-items-center justify-content-center min-vh-100">
    <div class="text-center" style="max-width: 460px; padding: 2rem;">
        <div class="card p-5">
            <div style="width: 80px; height: 80px; background: #FEF3C7; border-radius: 50%;
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
                <i class="bi bi-clock-history" style="font-size: 2.2rem; color: #F59E0B;"></i>
            </div>
            <h3 style="font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">Demasiadas solicitudes</h3>
            <p style="color: #6b7280; line-height: 1.7; margin-bottom: 2rem;">
                Has realizado demasiados intentos en poco tiempo.<br>
                Por favor espera unos minutos antes de intentar de nuevo.
            </p>
            <a href="/" class="btn btn-primary" style="border-radius: 8px; padding: 0.7rem 2rem;
                background: #5c8a3c; border-color: #5c8a3c; font-weight: 600;">
                <i class="bi bi-house me-2"></i>Volver al inicio
            </a>
        </div>
        <p style="color: #9ca3af; font-size: 0.8rem; margin-top: 1.5rem;">
            Error 429 — Fundación Rescate Animal
        </p>
    </div>
</body>
</html>"""
                        return HttpResponse(html, status=429, content_type='text/html; charset=utf-8')
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
