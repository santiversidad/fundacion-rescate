from django.shortcuts import render


def inicio(request):
    return render(request, 'institucional/inicio.html')


def nosotros(request):
    return render(request, 'institucional/nosotros.html')


def contacto(request):
    return render(request, 'institucional/contacto.html')