from django.db import models


class Mascota(models.Model):

    # Opciones fijas para campos de selección
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    ]

    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En proceso'),
        ('adoptada', 'Adoptada'),
        ('inactiva', 'Inactiva'),
    ]

    nombre        = models.CharField(max_length=100)
    especie       = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    raza          = models.CharField(max_length=100, blank=True)
    edad_anios    = models.PositiveIntegerField(default=0)
    sexo          = models.CharField(max_length=10, choices=SEXO_CHOICES)
    descripcion   = models.TextField(blank=True)
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    esterilizado  = models.BooleanField(default=False)
    vacunado      = models.BooleanField(default=False)
    fecha_ingreso = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} ({self.especie})'


class FotoMascota(models.Model):

    mascota      = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fotos')
    foto         = models.ImageField(upload_to='mascotas/')
    es_principal = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    def __str__(self):
        return f'Foto de {self.mascota.nombre}'