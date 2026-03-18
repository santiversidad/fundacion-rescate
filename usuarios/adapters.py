from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import requests as http_requests
from django.core.files.base import ContentFile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        email = data.get('email', '')
        if email:
            username = email.split('@')[0]
            username = username.replace('.', '_')
            user.username = username

        return user

    def save_user(self, request, sociallogin, form=None):
        from usuarios.models import PerfilUsuario
        user = super().save_user(request, sociallogin, form)

        try:
            extra_data = sociallogin.account.extra_data
            picture_url = extra_data.get('picture')

            if picture_url:
                response = http_requests.get(picture_url)
                if response.status_code == 200:
                    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
                    perfil.foto.save(
                        f'perfil_{user.username}.jpg',
                        ContentFile(response.content),
                        save=True
                    )
        except Exception as e:
            print(f'Error guardando foto: {e}')

        return user