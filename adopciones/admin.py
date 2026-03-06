from django.contrib import admin
from .models import SolicitudAdopcion


@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display  = ['usuario', 'mascota', 'estado', 'fecha_solicitud']
    list_filter   = ['estado', 'tipo_vivienda', 'tiene_otros_animales']
    search_fields = ['usuario__username', 'mascota__nombre']
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion']