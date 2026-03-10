from django.db import models


class MiembroEquipo(models.Model):
    nombre      = models.CharField(max_length=100)
    cargo       = models.CharField(max_length=100)
    foto        = models.ImageField(upload_to='equipo/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    orden       = models.PositiveIntegerField(default=0)
    activo      = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Miembro del equipo'
        verbose_name_plural = 'Equipo de trabajo'

    def __str__(self):
        return f'{self.nombre} — {self.cargo}'


class ContenidoNosotros(models.Model):
    mision      = models.TextField()
    vision      = models.TextField()
    imagen_mision = models.ImageField(upload_to='nosotros/', blank=True, null=True)
    imagen_vision = models.ImageField(upload_to='nosotros/', blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contenido Nosotros'
        verbose_name_plural = 'Contenido Nosotros'

    def __str__(self):
        return 'Contenido de la página Nosotros'