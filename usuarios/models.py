from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto  = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    bio   = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        return f'Perfil de {self.user.username}'