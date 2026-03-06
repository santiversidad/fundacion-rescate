from django.urls import path
from . import views

app_name = 'donaciones'

urlpatterns = [
    path('', views.info_donaciones, name='info'),
    path('registrar/', views.registrar_donacion, name='registrar'),
    path('mis-donaciones/', views.mis_donaciones, name='mis_donaciones'),
]