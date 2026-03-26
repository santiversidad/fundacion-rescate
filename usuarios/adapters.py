import logging
import urllib.parse
import requests as http_requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

MAX_AVATAR_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
ALLOWED_AVATAR_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
REQUEST_TIMEOUT_SECONDS = 10


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
                self._save_profile_picture(user, picture_url)
        except Exception as e:
            logger.warning('Error procesando datos de perfil social para usuario %s: %s', user.pk, e)

        return user

    def _save_profile_picture(self, user, picture_url):
        """Downloads and saves a profile picture from a trusted OAuth provider URL."""
        from usuarios.models import PerfilUsuario

        # Only allow HTTPS URLs to prevent SSRF
        parsed = urllib.parse.urlparse(picture_url)
        if parsed.scheme != 'https':
            logger.warning('Se rechazó URL de imagen no-HTTPS para usuario %s', user.pk)
            return

        try:
            response = http_requests.get(
                picture_url,
                timeout=REQUEST_TIMEOUT_SECONDS,
                stream=True,
                allow_redirects=False,  # Prevent redirect-based SSRF
            )
            response.raise_for_status()

            # Validate content type
            content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
            if content_type not in ALLOWED_AVATAR_CONTENT_TYPES:
                logger.warning(
                    'Tipo de contenido no permitido para foto de perfil (%s) del usuario %s',
                    content_type, user.pk
                )
                return

            # Read with size limit
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > MAX_AVATAR_SIZE_BYTES:
                    logger.warning(
                        'Foto de perfil excede tamaño máximo para usuario %s', user.pk
                    )
                    return

            perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
            perfil.foto.save(
                f'perfil_{user.username}.jpg',
                ContentFile(content),
                save=True
            )

        except http_requests.exceptions.Timeout:
            logger.warning('Timeout al descargar foto de perfil para usuario %s', user.pk)
        except http_requests.exceptions.RequestException as e:
            logger.warning('Error al descargar foto de perfil para usuario %s: %s', user.pk, e)