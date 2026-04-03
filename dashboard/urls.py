from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Mascotas
    path('mascotas/', views.mascotas, name='mascotas'),
    path('mascotas/agregar/', views.agregar_mascota, name='agregar_mascota'),
    path('mascotas/<int:pk>/editar/', views.editar_mascota, name='editar_mascota'),
    path('mascotas/<int:pk>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),

    # Adopciones
    path('adopciones/', views.adopciones, name='adopciones'),
    path('adopciones/<int:pk>/', views.detalle_adopcion, name='detalle_adopcion'),

    # Donaciones
    path('donaciones/', views.donaciones, name='donaciones'),
    path('donaciones/<int:pk>/', views.detalle_donacion, name='detalle_donacion'),

    # Eventos
    path('eventos/', views.eventos, name='eventos'),
    path('eventos/agregar/', views.agregar_evento, name='agregar_evento'),
    path('eventos/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),

    # Equipo
    path('equipo/', views.equipo, name='equipo'),
    path('equipo/agregar/', views.agregar_miembro, name='agregar_miembro'),
    path('equipo/<int:pk>/editar/', views.editar_miembro, name='editar_miembro'),
    path('equipo/<int:pk>/eliminar/', views.eliminar_miembro, name='eliminar_miembro'),

    # Testimonios
    path('testimonios/', views.testimonios, name='testimonios'),
    path('testimonios/<int:pk>/aprobar/', views.aprobar_testimonio, name='aprobar_testimonio'),
    path('testimonios/<int:pk>/rechazar/', views.rechazar_testimonio, name='rechazar_testimonio'),

    # Preguntas frecuentes
    path('faq/', views.faq, name='faq'),
    path('faq/agregar/', views.agregar_faq, name='agregar_faq'),
    path('faq/<int:pk>/editar/', views.editar_faq, name='editar_faq'),
    path('faq/<int:pk>/eliminar/', views.eliminar_faq, name='eliminar_faq'),

    # Contenido institucional
    path('institucional/', views.contenido_institucional, name='contenido_institucional'),

    # Mensajes de contacto
    path('mensajes/', views.mensajes, name='mensajes'),
    path('mensajes/<int:pk>/', views.marcar_mensaje_leido, name='detalle_mensaje'),

    # Usuarios registrados
    path('usuarios/', views.usuarios, name='usuarios'),
]