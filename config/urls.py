from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # ← nuevo
    path('', include('institucional.urls')),
    path('mascotas/', include('mascotas.urls')),
    path('adopciones/', include('adopciones.urls')),
    path('donaciones/', include('donaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)