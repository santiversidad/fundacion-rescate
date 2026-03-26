from django.db import models
from django.core.validators import MinValueValidator


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

class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=300)
    respuesta = models.TextField()
    orden     = models.PositiveIntegerField(default=0)
    activa    = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Pregunta frecuente'
        verbose_name_plural = 'Preguntas frecuentes'

    def __str__(self):
        return self.pregunta


class Testimonio(models.Model):
    nombre      = models.CharField(max_length=100)
    foto        = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    mensaje     = models.TextField()
    mascota     = models.CharField(max_length=100)
    fecha       = models.DateField(auto_now_add=True)
    aprobado    = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return f'{self.nombre} — {self.mascota}'


class Evento(models.Model):
    ESTADO_CHOICES = [
        ('proximo',    'Próximo'),
        ('en_curso',   'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado',  'Cancelado'),
    ]

    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen      = models.ImageField(upload_to='eventos/', blank=True, null=True)
    fecha       = models.DateTimeField()
    lugar       = models.CharField(max_length=200)
    capacidad   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    estado      = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='proximo', db_index=True)
    creado      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return self.titulo

    def cupos_disponibles(self):
        inscritos = self.inscripciones.count()
        return self.capacidad - inscritos

    def esta_lleno(self):
        return self.cupos_disponibles() <= 0


class InscripcionEvento(models.Model):
    evento   = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscripciones')
    usuario  = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['evento', 'usuario']
        verbose_name = 'Inscripción a evento'
        verbose_name_plural = 'Inscripciones a eventos'

    def __str__(self):
        return f'{self.usuario.username} — {self.evento.titulo}'