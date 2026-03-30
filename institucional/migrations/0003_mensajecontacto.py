from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0002_evento_preguntafrecuente_testimonio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensajeContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('asunto', models.CharField(max_length=200)),
                ('mensaje', models.TextField()),
                ('leido', models.BooleanField(default=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Mensaje de contacto',
                'verbose_name_plural': 'Mensajes de contacto',
                'ordering': ['-fecha'],
            },
        ),
    ]
