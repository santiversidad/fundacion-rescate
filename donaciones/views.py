from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donacion
from .forms import RegistrarDonacionForm
from config.middleware import rate_limit


@login_required
def info_donaciones(request):
    return render(request, 'donaciones/info.html')


@login_required
@rate_limit(max_requests=10, window_seconds=3600, key_prefix='donacion')
def registrar_donacion(request):
    if request.method == 'POST':
        form = RegistrarDonacionForm(request.POST, request.FILES)
        if form.is_valid():
            Donacion.objects.create(
                usuario=request.user,
                monto=form.cleaned_data['monto'],
                metodo=form.cleaned_data['metodo'],
                fecha_donacion=form.cleaned_data['fecha_donacion'],
                comprobante=form.cleaned_data.get('comprobante'),
            )
            messages.success(request, '✅ Tu donación fue registrada correctamente. La verificaremos en 24 horas.')
            return redirect('donaciones:mis_donaciones')
    else:
        form = RegistrarDonacionForm()

    return render(request, 'donaciones/registrar.html', {'form': form})


@login_required
def mis_donaciones(request):
    donaciones = Donacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha_donacion')
    return render(request, 'donaciones/mis_donaciones.html', {
        'donaciones': donaciones
    })
