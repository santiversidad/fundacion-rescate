import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Donacion


def validate_image_upload(file):
    if file is None:
        return
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    max_size = 5 * 1024 * 1024  # 5MB
    if hasattr(file, 'content_type') and file.content_type not in allowed_types:
        raise ValidationError('Solo se permiten imágenes (JPEG, PNG, WebP, GIF).')
    if file.size > max_size:
        raise ValidationError('El archivo no puede superar los 5MB.')


class RegistrarDonacionForm(forms.Form):
    METODO_CHOICES = Donacion.METODO_CHOICES

    monto = forms.DecimalField(
        min_value=1,
        max_value=100000000,
        decimal_places=2,
        error_messages={
            'required': 'Ingresa el monto donado.',
            'min_value': 'El monto debe ser mayor a 0.',
            'invalid': 'Ingresa un monto válido.',
        }
    )
    metodo = forms.ChoiceField(
        choices=METODO_CHOICES,
        error_messages={'required': 'Selecciona el método de donación.'}
    )
    fecha_donacion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={
            'required': 'Ingresa la fecha de la donación.',
            'invalid': 'Ingresa una fecha válida.',
        }
    )
    comprobante = forms.ImageField(
        required=False,
        validators=[validate_image_upload],
        error_messages={'invalid_image': 'El archivo debe ser una imagen válida.'}
    )

    def clean_fecha_donacion(self):
        fecha = self.cleaned_data.get('fecha_donacion')
        if fecha and fecha > datetime.date.today():
            raise forms.ValidationError('La fecha de donación no puede ser futura.')
        return fecha