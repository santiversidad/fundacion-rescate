from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0002_alter_mascota_fecha_ingreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotomascota',
            name='alt_text',
            field=models.CharField(
                blank=True,
                max_length=200,
                help_text='Descripción breve de la imagen para accesibilidad y SEO.',
            ),
        ),
    ]