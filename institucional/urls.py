from django.urls import path
from . import views

app_name = 'institucional'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('como-ayudar/', views.como_ayudar, name='como_ayudar'),
    path('preguntas-frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('eventos/', views.eventos, name='eventos'),
    path('eventos/<int:pk>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:pk>/inscribirse/', views.inscribirse_evento, name='inscribirse_evento'),
]