from django.contrib import admin
from .models import RegistroActividad


@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modelo', 'descripcion', 'fecha')
    list_filter = ('accion', 'modelo', 'fecha')
    search_fields = ('descripcion', 'usuario__username')
    readonly_fields = ('usuario', 'accion', 'modelo', 'objeto_id', 'descripcion', 'fecha')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
