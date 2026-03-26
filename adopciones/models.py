from django.db import models
from django.contrib.auth.models import User
from mascotas.models import Mascota


class SolicitudAdopcion(models.Model):

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    VIVIENDA_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('finca', 'Finca'),
        ('otro', 'Otro'),
    ]

    usuario             = models.ForeignKey(User, on_delete=models.CASCADE)
    mascota             = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    motivo              = models.TextField()
    tipo_vivienda       = models.CharField(max_length=20, choices=VIVIENDA_CHOICES)
    tiene_otros_animales = models.BooleanField(default=False)
    estado              = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', db_index=True)
    fecha_solicitud     = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    observaciones_admin = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Solicitud de Adopción'
        verbose_name_plural = 'Solicitudes de Adopción'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f'{self.usuario.username} → {self.mascota.nombre}'