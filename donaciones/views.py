from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Donacion


@login_required
def info_donaciones(request):
    return render(request, 'donaciones/info.html')


@login_required
def registrar_donacion(request):
    if request.method == 'POST':
        Donacion.objects.create(
            usuario=request.user,
            monto=request.POST['monto'],
            metodo=request.POST['metodo'],
            fecha_donacion=request.POST['fecha_donacion'],
            comprobante=request.FILES.get('comprobante'),
        )
        return redirect('donaciones:mis_donaciones')

    return render(request, 'donaciones/registrar.html')


@login_required
def mis_donaciones(request):
    donaciones = Donacion.objects.filter(usuario=request.user)
    return render(request, 'donaciones/mis_donaciones.html', {
        'donaciones': donaciones
    })