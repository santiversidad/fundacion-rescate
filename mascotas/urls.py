from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('<int:pk>/', views.detalle_mascota, name='detalle'),
]