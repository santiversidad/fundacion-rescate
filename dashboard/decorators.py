from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '⚠️ Debes iniciar sesión para acceder.')
            return redirect('usuarios:login')
        if not request.user.is_staff:
            messages.error(request, '❌ No tienes permisos para acceder a esta sección.')
            return redirect('institucional:inicio')
        return view_func(request, *args, **kwargs)
    return wrapper