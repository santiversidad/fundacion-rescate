from django.contrib import admin
from .models import (
    MiembroEquipo,
    ContenidoNosotros,
    PreguntaFrecuente,
    Testimonio,
    Evento,
    InscripcionEvento,
)


@admin.register(MiembroEquipo)
class MiembroEquipoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'cargo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    search_fields = ['nombre', 'cargo']


@admin.register(ContenidoNosotros)
class ContenidoNosotrosAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display  = ['pregunta', 'orden', 'activa']
    list_editable = ['orden', 'activa']
    search_fields = ['pregunta']


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display    = ['nombre', 'mascota', 'fecha', 'aprobado']
    list_editable   = ['aprobado']
    search_fields   = ['nombre', 'mascota']
    readonly_fields = ['fecha']


class InscripcionEventoInline(admin.TabularInline):
    model           = InscripcionEvento
    readonly_fields = ['usuario', 'fecha']
    extra           = 0


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'fecha', 'lugar', 'estado', 'capacidad']
    list_filter   = ['estado']
    search_fields = ['titulo', 'lugar']
    inlines       = [InscripcionEventoInline]