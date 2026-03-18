from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Generar username automático desde el correo
        email = data.get('email', '')
        if email:
            username = email.split('@')[0]
            # Reemplazar puntos por guiones bajos
            username = username.replace('.', '_')
            user.username = username

        return user