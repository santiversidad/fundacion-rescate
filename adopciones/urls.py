from django.urls import path
from . import views

app_name = 'adopciones'

urlpatterns = [
    path('solicitar/<int:mascota_pk>/', views.solicitar_adopcion, name='solicitar'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
]