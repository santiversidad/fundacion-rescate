from django.contrib import admin
from .models import Donacion


@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display  = ['usuario', 'monto', 'metodo', 'estado', 'fecha_donacion']
    list_filter   = ['estado', 'metodo']
    search_fields = ['usuario__username']
    readonly_fields = ['fecha_registro']