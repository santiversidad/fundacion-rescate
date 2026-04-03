from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from config.middleware import rate_limit
from .forms import RegistroForm, UserUpdateForm, PerfilUsuarioForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('usuarios:perfil')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@rate_limit(max_requests=5, window_seconds=300, key_prefix='login')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('institucional:inicio')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('institucional:inicio')


@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')


@login_required
def editar_perfil(request):
    perfil_obj, _ = request.user.__class__.objects.get_or_create(
        pk=request.user.pk
    )
    # Get or create PerfilUsuario
    from .models import PerfilUsuario as PerfilModel
    perfil_inst, _ = PerfilModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_inst)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('usuarios:perfil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil_inst)

    return render(request, 'usuarios/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })
