from django.db import models
from django.contrib.auth.models import User


class RegistroActividad(models.Model):
    """Tracks admin actions in the dashboard for accountability."""

    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('aprobar', 'Aprobar'),
        ('rechazar', 'Rechazar'),
        ('verificar', 'Verificar'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    modelo = models.CharField(max_length=50)  # e.g., 'Mascota', 'Donacion'
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Registro de actividad'
        verbose_name_plural = 'Registro de actividades'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario} — {self.accion} {self.modelo} — {self.fecha:%d/%m/%Y %H:%M}'