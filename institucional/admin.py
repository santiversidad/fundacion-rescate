from django.contrib import admin
from .models import MiembroEquipo, ContenidoNosotros


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