from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from institucional.sitemaps import StaticViewSitemap, MascotaSitemap

handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'

sitemaps = {
    'static': StaticViewSitemap,
    'mascotas': MascotaSitemap,
}

urlpatterns = [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('institucional.urls')),
    path('mascotas/', include('mascotas.urls')),
    path('adopciones/', include('adopciones.urls')),
    path('donaciones/', include('donaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)