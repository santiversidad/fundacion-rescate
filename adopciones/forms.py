from django import forms
from .models import SolicitudAdopcion


class SolicitudAdopcionForm(forms.Form):
    TIPO_VIVIENDA_CHOICES = SolicitudAdopcion.VIVIENDA_CHOICES

    motivo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 1000}),
        min_length=20,
        max_length=1000,
        error_messages={
            'required': 'Por favor explica por qué quieres adoptar esta mascota.',
            'min_length': 'El motivo debe tener al menos 20 caracteres.',
        }
    )
    tipo_vivienda = forms.ChoiceField(
        choices=TIPO_VIVIENDA_CHOICES,
        error_messages={'required': 'Selecciona el tipo de vivienda.'}
    )
    tiene_otros_animales = forms.BooleanField(required=False)
