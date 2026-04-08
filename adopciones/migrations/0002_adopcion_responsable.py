# Migración: Proceso de adopción responsable
# Agrega campos de evaluación del adoptante, nuevos estados y campos de gestión.
# Todos los nuevos campos son blank=True o tienen default → compatibles con datos existentes.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0001_initial'),
    ]

    operations = [

        # ── Actualizar ESTADO_CHOICES ─────────────────────────────────────────
        migrations.AlterField(
            model_name='solicitudadopcion',
            name='estado',
            field=models.CharField(
                choices=[
                    ('pendiente',   'Pendiente de revisión'),
                    ('en_revision', 'En revisión'),
                    ('entrevista',  'Entrevista programada'),
                    ('aprobada',    'Aprobada'),
                    ('rechazada',   'No aprobada'),
                    ('completada',  'Adopción completada'),
                    ('cancelada',   'Cancelada por el solicitante'),
                ],
                default='pendiente',
                max_length=20,
                db_index=True,
            ),
        ),

        # ── Actualizar tipo_vivienda para que sea blank=True ─────────────────
        migrations.AlterField(
            model_name='solicitudadopcion',
            name='tipo_vivienda',
            field=models.CharField(
                choices=[
                    ('casa',        'Casa'),
                    ('apartamento', 'Apartamento'),
                    ('finca',       'Finca'),
                    ('otro',        'Otro'),
                ],
                max_length=20,
                blank=True,
            ),
        ),

        # ── Actualizar motivo para que sea blank=True ─────────────────────────
        migrations.AlterField(
            model_name='solicitudadopcion',
            name='motivo',
            field=models.TextField(blank=True),
        ),

        # ── Sección 1: Información de contacto ───────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='nombre_completo',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='telefono',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='ciudad',
            field=models.CharField(max_length=100, blank=True),
        ),

        # ── Sección 2: Información del hogar ─────────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='vivienda_propia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='permiso_arrendador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='tiene_patio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='patio_cercado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='personas_en_hogar',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='ninos_en_hogar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='edad_ninos',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='alguien_alergico',
            field=models.BooleanField(default=False),
        ),

        # ── Sección 3: Experiencia con animales ───────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='descripcion_otros_animales',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='experiencia_previa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='que_paso_mascotas_anteriores',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='veterinario_referencia',
            field=models.CharField(max_length=200, blank=True),
        ),

        # ── Sección 4: Estilo de vida ─────────────────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='horas_fuera_casa',
            field=models.CharField(
                max_length=10,
                choices=[
                    ('menos_4', 'Menos de 4 horas'),
                    ('4_8',     'Entre 4 y 8 horas'),
                    ('8_12',    'Entre 8 y 12 horas'),
                    ('mas_12',  'Más de 12 horas'),
                ],
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='nivel_actividad',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('sedentario',  'Sedentario (poco ejercicio)'),
                    ('moderado',    'Moderado (caminatas regulares)'),
                    ('activo',      'Activo (ejercicio frecuente)'),
                    ('muy_activo',  'Muy activo (deporte diario)'),
                ],
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='viaja_frecuentemente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='plan_cuidado_viajes',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='presupuesto_veterinario',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('basico',   'Básico — hasta $100.000/mes'),
                    ('moderado', 'Moderado — $100.000–$300.000/mes'),
                    ('amplio',   'Amplio — más de $300.000/mes'),
                ],
                blank=True,
            ),
        ),

        # ── Sección 5: Compromisos ────────────────────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='compromiso_veterinario',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='compromiso_no_abandono',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='acepta_seguimiento',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='acepta_terminos',
            field=models.BooleanField(default=False),
        ),

        # ── Campos administrativos ────────────────────────────────────────────
        migrations.AddField(
            model_name='solicitudadopcion',
            name='fecha_entrevista',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='notas_entrevista',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='solicitudadopcion',
            name='fecha_resolucion',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]