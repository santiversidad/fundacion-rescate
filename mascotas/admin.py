from django.contrib import admin
from .models import Mascota, FotoMascota


class FotoMascotaInline(admin.TabularInline):
    model = FotoMascota
    extra = 3


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'especie', 'sexo', 'estado', 'fecha_ingreso']
    list_filter   = ['especie', 'estado', 'sexo', 'esterilizado', 'vacunado']
    search_fields = ['nombre', 'raza', 'descripcion']
    inlines       = [FotoMascotaInline]