import os
from django import forms
from django.core.exceptions import ValidationError
from mascotas.models import Mascota
from institucional.models import Evento, MiembroEquipo, PreguntaFrecuente, ContenidoNosotros


def validate_image_file(file):
    if file is None:
        return
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    max_size = 5 * 1024 * 1024  # 5MB
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError('Solo se permiten imágenes (JPG, PNG, WebP, GIF).')
    if file.size > max_size:
        raise ValidationError('La imagen no puede superar los 5MB.')


class MascotaForm(forms.Form):
    nombre = forms.CharField(max_length=100, error_messages={'required': 'El nombre es obligatorio.'})
    especie = forms.ChoiceField(choices=Mascota.ESPECIE_CHOICES, error_messages={'required': 'Selecciona la especie.'})
    raza = forms.CharField(max_length=100, required=False)
    edad_anios = forms.IntegerField(
        min_value=0, max_value=30,
        error_messages={
            'required': 'La edad es obligatoria.',
            'min_value': 'La edad no puede ser negativa.',
            'max_value': 'Verifica la edad ingresada.',
            'invalid': 'Ingresa un número entero para la edad.',
        }
    )
    sexo = forms.ChoiceField(choices=Mascota.SEXO_CHOICES, error_messages={'required': 'Selecciona el sexo.'})
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False, max_length=2000
    )
    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': 'La fecha de ingreso es obligatoria.', 'invalid': 'Fecha inválida.'}
    )
    esterilizado = forms.BooleanField(required=False)
    vacunado = forms.BooleanField(required=False)
    estado = forms.ChoiceField(choices=Mascota.ESTADO_CHOICES, required=False)


class EventoForm(forms.Form):
    titulo = forms.CharField(max_length=200, error_messages={'required': 'El título es obligatorio.'})
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        error_messages={'required': 'La descripción es obligatoria.'}
    )
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        error_messages={'required': 'La fecha del evento es obligatoria.', 'invalid': 'Fecha/hora inválida.'}
    )
    lugar = forms.CharField(max_length=300, error_messages={'required': 'El lugar es obligatorio.'})
    capacidad = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': 'La capacidad es obligatoria.',
            'min_value': 'La capacidad debe ser al menos 1.',
            'invalid': 'Ingresa un número entero para la capacidad.',
        }
    )
    imagen = forms.ImageField(required=False, validators=[validate_image_file])
    estado = forms.ChoiceField(choices=Evento.ESTADO_CHOICES, required=False)


class MiembroEquipoForm(forms.Form):
    nombre = forms.CharField(max_length=200, error_messages={'required': 'El nombre es obligatorio.'})
    cargo = forms.CharField(max_length=200, error_messages={'required': 'El cargo es obligatorio.'})
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False, max_length=1000
    )
    orden = forms.IntegerField(min_value=0, required=False, initial=0)
    foto = forms.ImageField(required=False, validators=[validate_image_file])
    activo = forms.BooleanField(required=False)


class PreguntaFrecuenteForm(forms.Form):
    pregunta = forms.CharField(max_length=500, error_messages={'required': 'La pregunta es obligatoria.'})
    respuesta = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        error_messages={'required': 'La respuesta es obligatoria.'}
    )
    orden = forms.IntegerField(min_value=0, required=False, initial=0)
    activa = forms.BooleanField(required=False)


class ContenidoNosotrosForm(forms.Form):
    mision = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        error_messages={'required': 'La misión es obligatoria.'}
    )
    vision = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        error_messages={'required': 'La visión es obligatoria.'}
    )
    imagen_mision = forms.ImageField(required=False, validators=[validate_image_file])
    imagen_vision = forms.ImageField(required=False, validators=[validate_image_file])


class AdopcionEstadoForm(forms.Form):
    from adopciones.models import SolicitudAdopcion
    estado = forms.ChoiceField(choices=SolicitudAdopcion.ESTADO_CHOICES)
    observaciones_admin = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False, max_length=1000
    )


class DonacionEstadoForm(forms.Form):
    from donaciones.models import Donacion
    estado = forms.ChoiceField(choices=Donacion.ESTADO_CHOICES)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False, max_length=1000
    )
