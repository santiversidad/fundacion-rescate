from django import forms
from .models import SolicitudAdopcion


class SolicitudAdopcionForm(forms.Form):
    """
    Formulario de solicitud de adopción responsable.
    5 secciones que evalúan al adoptante de forma integral.
    """

    # ── SECCIÓN 1: INFORMACIÓN PERSONAL ──────────────────────────────────────

    nombre_completo = forms.CharField(
        max_length=200,
        label='Nombre completo',
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre y apellido completo'}),
        error_messages={'required': 'Tu nombre completo es obligatorio.'},
    )
    telefono = forms.CharField(
        max_length=20,
        label='Teléfono de contacto',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 300 123 4567'}),
        error_messages={'required': 'El teléfono de contacto es obligatorio.'},
    )
    ciudad = forms.CharField(
        max_length=100,
        label='Ciudad de residencia',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Bogotá, Medellín, Cali...'}),
        error_messages={'required': 'La ciudad de residencia es obligatoria.'},
    )

    # ── SECCIÓN 2: INFORMACIÓN DEL HOGAR ─────────────────────────────────────

    tipo_vivienda = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + SolicitudAdopcion.VIVIENDA_CHOICES,
        label='Tipo de vivienda',
        error_messages={'required': 'Selecciona el tipo de vivienda.'},
    )
    vivienda_propia = forms.BooleanField(
        required=False,
        label='La vivienda es propia',
    )
    permiso_arrendador = forms.BooleanField(
        required=False,
        label='Cuento con permiso del arrendador para tener mascotas',
    )
    tiene_patio = forms.BooleanField(
        required=False,
        label='La vivienda tiene patio o zona exterior',
    )
    patio_cercado = forms.BooleanField(
        required=False,
        label='El patio / zona exterior está cercado/a de forma segura',
    )
    personas_en_hogar = forms.IntegerField(
        min_value=1,
        max_value=20,
        label='Número de personas que viven en el hogar',
        widget=forms.NumberInput(attrs={'min': '1', 'max': '20'}),
        error_messages={
            'required': 'Indica cuántas personas viven en el hogar.',
            'min_value': 'Debe haber al menos 1 persona.',
        },
    )
    ninos_en_hogar = forms.BooleanField(
        required=False,
        label='Hay niños menores de 12 años en el hogar',
    )
    edad_ninos = forms.CharField(
        max_length=100,
        required=False,
        label='Edades de los niños',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 4, 7 y 10 años'}),
    )
    alguien_alergico = forms.BooleanField(
        required=False,
        label='Algún integrante del hogar tiene alergia a los animales',
    )

    # ── SECCIÓN 3: EXPERIENCIA CON ANIMALES ──────────────────────────────────

    tiene_otros_animales = forms.BooleanField(
        required=False,
        label='Actualmente tengo otras mascotas en casa',
    )
    descripcion_otros_animales = forms.CharField(
        max_length=300,
        required=False,
        label='Describe tus mascotas actuales',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Especie, raza, edad, si están esterilizados...',
        }),
    )
    experiencia_previa = forms.BooleanField(
        required=False,
        label='He tenido mascotas anteriormente',
    )
    que_paso_mascotas_anteriores = forms.CharField(
        max_length=600,
        required=False,
        label='¿Qué pasó con tus mascotas anteriores?',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': (
                'Cuéntanos con honestidad. No hay respuestas incorrectas — '
                'esta información nos ayuda a hacer el mejor match.'
            ),
        }),
    )
    veterinario_referencia = forms.CharField(
        max_length=200,
        required=False,
        label='Veterinario/a de confianza (nombre o clínica)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre o clínica veterinaria que ya conoces',
        }),
    )

    # ── SECCIÓN 4: ESTILO DE VIDA ─────────────────────────────────────────────

    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'maxlength': 1000,
            'placeholder': (
                'Cuéntanos por qué deseas ser guardián/a de este animal. '
                'Qué cambios esperas que traiga a tu vida y qué puedes ofrecerle.'
            ),
        }),
        min_length=30,
        max_length=1000,
        label='¿Por qué deseas iniciar este proceso de adopción?',
        error_messages={
            'required': 'Por favor cuéntanos tu motivación para adoptar.',
            'min_length': 'Cuéntanos un poco más — mínimo 30 caracteres.',
        },
    )
    horas_fuera_casa = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + SolicitudAdopcion.HORAS_SOLO_CHOICES,
        label='¿Cuántas horas al día sueles estar fuera de casa?',
        error_messages={'required': 'Indica cuántas horas estás fuera de casa.'},
    )
    nivel_actividad = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + SolicitudAdopcion.ACTIVIDAD_CHOICES,
        label='¿Cómo describirías tu nivel de actividad física?',
        error_messages={'required': 'Selecciona tu nivel de actividad.'},
    )
    viaja_frecuentemente = forms.BooleanField(
        required=False,
        label='Viajo frecuentemente (más de una semana al mes)',
    )
    plan_cuidado_viajes = forms.CharField(
        max_length=300,
        required=False,
        label='Plan de cuidado del animal durante tus viajes',
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Ej: Familiar en la ciudad, guardería de mascotas de confianza...',
        }),
    )
    presupuesto_veterinario = forms.ChoiceField(
        choices=[('', 'Selecciona una opción')] + SolicitudAdopcion.PRESUPUESTO_CHOICES,
        label='¿Cuánto podrías destinar mensualmente al cuidado veterinario?',
        error_messages={'required': 'Selecciona un rango de presupuesto.'},
    )

    # ── SECCIÓN 5: COMPROMISOS DEL ADOPTANTE ─────────────────────────────────

    compromiso_veterinario = forms.BooleanField(
        required=True,
        label=(
            'Me comprometo a proporcionar atención veterinaria oportuna '
            '(vacunas, controles, esterilización si aplica y atención ante enfermedades).'
        ),
        error_messages={'required': 'Debes confirmar el compromiso de atención veterinaria.'},
    )
    compromiso_no_abandono = forms.BooleanField(
        required=True,
        label=(
            'Me comprometo a no abandonar, ceder ni transferir el animal sin '
            'coordinación previa con la Fundación Rescate Animal.'
        ),
        error_messages={'required': 'Debes confirmar el compromiso de no abandono.'},
    )
    acepta_seguimiento = forms.BooleanField(
        required=True,
        label=(
            'Acepto recibir visitas de seguimiento post-adopción '
            '(a los 30 días, 3 meses y 1 año) para verificar el bienestar del animal.'
        ),
        error_messages={'required': 'Debes aceptar el seguimiento post-adopción.'},
    )
    acepta_terminos = forms.BooleanField(
        required=True,
        label=(
            'He leído, entiendo y acepto los términos del proceso de adopción '
            'responsable de la Fundación Rescate Animal.'
        ),
        error_messages={'required': 'Debes aceptar los términos del proceso de adopción.'},
    )

    # ── BOOTSTRAP CLASSES ────────────────────────────────────────────────────

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault('class', 'form-select')
            else:
                widget.attrs.setdefault('class', 'form-control')

    # ── VALIDACIONES CRUZADAS ────────────────────────────────────────────────

    def clean(self):
        cleaned = super().clean()

        if cleaned.get('viaja_frecuentemente') and not cleaned.get('plan_cuidado_viajes', '').strip():
            self.add_error(
                'plan_cuidado_viajes',
                'Si viajas frecuentemente, describe tu plan de cuidado durante los viajes.',
            )

        if cleaned.get('tiene_otros_animales') and not cleaned.get('descripcion_otros_animales', '').strip():
            self.add_error(
                'descripcion_otros_animales',
                'Por favor describe brevemente tus mascotas actuales.',
            )

        if cleaned.get('ninos_en_hogar') and not cleaned.get('edad_ninos', '').strip():
            self.add_error(
                'edad_ninos',
                'Indica las edades de los niños en el hogar.',
            )

        return cleaned