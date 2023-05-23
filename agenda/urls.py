from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index_agenda, name='index_agenda'),
    path('diaria/', views.index_diario, name='index_diario'),
    path('diaria/hora/', views.index_hora, name = 'index_horaria'),
    path('generar_semana/', views.generar_semana, name='generar_semana')
]