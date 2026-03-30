from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from mascotas.models import Mascota


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'institucional:inicio',
            'institucional:nosotros',
            'institucional:contacto',
            'institucional:como_ayudar',
            'institucional:preguntas_frecuentes',
            'institucional:testimonios',
            'institucional:eventos',
            'mascotas:catalogo',
            'donaciones:info',
        ]

    def location(self, item):
        return reverse(item)


class MascotaSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return Mascota.objects.filter(estado='disponible')

    def location(self, mascota):
        return reverse('mascotas:detalle', args=[mascota.pk])

    def lastmod(self, mascota):
        return mascota.fecha_registro