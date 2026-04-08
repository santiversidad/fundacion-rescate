from django.contrib import admin
from .models import SolicitudAdopcion


@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display  = ['usuario', 'mascota', 'estado', 'ciudad', 'fecha_solicitud', 'fecha_entrevista']
    list_filter   = ['estado', 'tipo_vivienda', 'tiene_otros_animales', 'vivienda_propia', 'ninos_en_hogar']
    search_fields = ['usuario__username', 'mascota__nombre', 'nombre_completo', 'ciudad', 'telefono']
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion', 'fecha_resolucion']
    fieldsets = (
        ('Estado', {
            'fields': ('estado', 'observaciones_admin', 'fecha_entrevista', 'notas_entrevista', 'fecha_resolucion'),
        }),
        ('Solicitud', {
            'fields': ('usuario', 'mascota', 'fecha_solicitud', 'fecha_actualizacion'),
        }),
        ('Contacto', {
            'fields': ('nombre_completo', 'telefono', 'ciudad'),
        }),
        ('Hogar', {
            'fields': ('tipo_vivienda', 'vivienda_propia', 'permiso_arrendador',
                        'tiene_patio', 'patio_cercado', 'personas_en_hogar',
                        'ninos_en_hogar', 'edad_ninos', 'alguien_alergico'),
        }),
        ('Experiencia con animales', {
            'fields': ('tiene_otros_animales', 'descripcion_otros_animales',
                        'experiencia_previa', 'que_paso_mascotas_anteriores',
                        'veterinario_referencia'),
        }),
        ('Estilo de vida', {
            'fields': ('motivo', 'horas_fuera_casa', 'nivel_actividad',
                        'viaja_frecuentemente', 'plan_cuidado_viajes',
                        'presupuesto_veterinario'),
        }),
        ('Compromisos', {
            'fields': ('compromiso_veterinario', 'compromiso_no_abandono',
                        'acepta_seguimiento', 'acepta_terminos'),
        }),
    )