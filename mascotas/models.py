from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


def validar_fecha_ingreso(fecha):
    hoy = timezone.now().date()
    minima = hoy - timedelta(days=7)
    maxima = hoy + timedelta(days=30)

    if fecha < minima:
        raise ValidationError(
            f'La fecha de ingreso no puede ser anterior a {minima.strftime("%d/%m/%Y")}. '
            f'Solo se permiten fechas desde 7 días atrás.'
        )
    if fecha > maxima:
        raise ValidationError(
            f'La fecha de ingreso no puede ser posterior a {maxima.strftime("%d/%m/%Y")}. '
            f'Solo se permiten fechas hasta 30 días en el futuro.'
        )

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
    especie       = models.CharField(max_length=10, choices=ESPECIE_CHOICES, db_index=True)
    raza          = models.CharField(max_length=100, blank=True)
    edad_anios    = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
    sexo          = models.CharField(max_length=10, choices=SEXO_CHOICES)
    descripcion   = models.TextField(blank=True)
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', db_index=True)
    esterilizado  = models.BooleanField(default=False)
    vacunado      = models.BooleanField(default=False)
    fecha_ingreso = models.DateField(validators=[validar_fecha_ingreso])
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