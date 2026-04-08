from django.db import models
from django.contrib.auth.models import User
from mascotas.models import Mascota


class SolicitudAdopcion(models.Model):

    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente de revisión'),
        ('en_revision', 'En revisión'),
        ('entrevista',  'Entrevista programada'),
        ('aprobada',    'Aprobada'),
        ('rechazada',   'No aprobada'),
        ('completada',  'Adopción completada'),
        ('cancelada',   'Cancelada por el solicitante'),
    ]

    VIVIENDA_CHOICES = [
        ('casa',        'Casa'),
        ('apartamento', 'Apartamento'),
        ('finca',       'Finca'),
        ('otro',        'Otro'),
    ]

    HORAS_SOLO_CHOICES = [
        ('menos_4', 'Menos de 4 horas'),
        ('4_8',     'Entre 4 y 8 horas'),
        ('8_12',    'Entre 8 y 12 horas'),
        ('mas_12',  'Más de 12 horas'),
    ]

    ACTIVIDAD_CHOICES = [
        ('sedentario',  'Sedentario (poco ejercicio)'),
        ('moderado',    'Moderado (caminatas regulares)'),
        ('activo',      'Activo (ejercicio frecuente)'),
        ('muy_activo',  'Muy activo (deporte diario)'),
    ]

    PRESUPUESTO_CHOICES = [
        ('basico',    'Básico — hasta $100.000/mes'),
        ('moderado',  'Moderado — $100.000–$300.000/mes'),
        ('amplio',    'Amplio — más de $300.000/mes'),
    ]

    # ── Relaciones ────────────────────────────────────────────────────────────
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    mascota  = models.ForeignKey(Mascota, on_delete=models.CASCADE)

    # ── Sección 1: Información de contacto ───────────────────────────────────
    nombre_completo = models.CharField(max_length=200, blank=True)
    telefono        = models.CharField(max_length=20, blank=True)
    ciudad          = models.CharField(max_length=100, blank=True)

    # ── Sección 2: Información del hogar ─────────────────────────────────────
    tipo_vivienda      = models.CharField(max_length=20, choices=VIVIENDA_CHOICES, blank=True)
    vivienda_propia    = models.BooleanField(default=False)
    permiso_arrendador = models.BooleanField(default=False)
    tiene_patio        = models.BooleanField(default=False)
    patio_cercado      = models.BooleanField(default=False)
    personas_en_hogar  = models.PositiveSmallIntegerField(default=1)
    ninos_en_hogar     = models.BooleanField(default=False)
    edad_ninos         = models.CharField(max_length=100, blank=True)
    alguien_alergico   = models.BooleanField(default=False)

    # ── Sección 3: Experiencia con animales ───────────────────────────────────
    tiene_otros_animales         = models.BooleanField(default=False)
    descripcion_otros_animales   = models.CharField(max_length=300, blank=True)
    experiencia_previa           = models.BooleanField(default=False)
    que_paso_mascotas_anteriores = models.TextField(blank=True)
    veterinario_referencia       = models.CharField(max_length=200, blank=True)

    # ── Sección 4: Estilo de vida ─────────────────────────────────────────────
    motivo                  = models.TextField(blank=True)
    horas_fuera_casa        = models.CharField(max_length=10, choices=HORAS_SOLO_CHOICES, blank=True)
    nivel_actividad         = models.CharField(max_length=20, choices=ACTIVIDAD_CHOICES, blank=True)
    viaja_frecuentemente    = models.BooleanField(default=False)
    plan_cuidado_viajes     = models.CharField(max_length=300, blank=True)
    presupuesto_veterinario = models.CharField(max_length=20, choices=PRESUPUESTO_CHOICES, blank=True)

    # ── Sección 5: Compromisos del adoptante ──────────────────────────────────
    compromiso_veterinario  = models.BooleanField(default=False)
    compromiso_no_abandono  = models.BooleanField(default=False)
    acepta_seguimiento      = models.BooleanField(default=False)
    acepta_terminos         = models.BooleanField(default=False)

    # ── Estado y gestión ──────────────────────────────────────────────────────
    estado              = models.CharField(max_length=20, choices=ESTADO_CHOICES,
                                            default='pendiente', db_index=True)
    observaciones_admin = models.TextField(blank=True)
    fecha_entrevista    = models.DateTimeField(null=True, blank=True)
    notas_entrevista    = models.TextField(blank=True)
    fecha_resolucion    = models.DateTimeField(null=True, blank=True)

    # ── Auditoría ─────────────────────────────────────────────────────────────
    fecha_solicitud     = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Solicitud de Adopción'
        verbose_name_plural = 'Solicitudes de Adopción'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f'{self.usuario.username} → {self.mascota.nombre}'

    @property
    def foto_principal(self):
        return (
            self.mascota.fotos.filter(es_principal=True).first()
            or self.mascota.fotos.first()
        )