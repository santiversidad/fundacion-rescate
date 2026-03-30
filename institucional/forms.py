from django import forms
from .models import MensajeContacto, Testimonio
from usuarios.validators import validate_image_file


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre':  forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'email':   forms.EmailInput(attrs={'placeholder': 'tucorreo@gmail.com'}),
            'asunto':  forms.TextInput(attrs={'placeholder': '¿En qué podemos ayudarte?'}),
            'mensaje': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
        labels = {
            'nombre':  'Nombre',
            'email':   'Correo electrónico',
            'asunto':  'Asunto',
            'mensaje': 'Mensaje',
        }


class TestimonioPublicoForm(forms.ModelForm):
    foto = forms.ImageField(required=False, validators=[validate_image_file])

    class Meta:
        model = Testimonio
        fields = ['nombre', 'mascota', 'mensaje', 'foto']
        widgets = {
            'nombre':  forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'mascota': forms.TextInput(attrs={'placeholder': 'Nombre de la mascota que adoptaste'}),
            'mensaje': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Cuéntanos tu experiencia de adopción...',
            }),
        }
        labels = {
            'nombre':  'Tu nombre',
            'mascota': 'Mascota adoptada',
            'mensaje': 'Tu historia',
            'foto':    'Foto tuya o de tu mascota (opcional)',
        }
