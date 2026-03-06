from django.db import models
from django.contrib.auth.models import User


class Donacion(models.Model):

    METODO_CHOICES = [
        ('transferencia', 'Transferencia bancaria'),
        ('deposito', 'Depósito bancario'),
        ('efectivo', 'Efectivo'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de verificación'),
        ('verificada', 'Verificada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario         = models.ForeignKey(User, on_delete=models.CASCADE)
    monto           = models.DecimalField(max_digits=10, decimal_places=2)
    metodo          = models.CharField(max_length=20, choices=METODO_CHOICES)
    comprobante     = models.ImageField(upload_to='comprobantes/', blank=True)
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_donacion  = models.DateField()
    fecha_registro  = models.DateTimeField(auto_now_add=True)
    observaciones   = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.usuario.username} — ${self.monto}'