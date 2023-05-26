from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index_agenda, name='index_agenda'),
    path('dia/<str:fecha>', views.index_diario, name='index_diario'),
    path('dia/turno/<int:id>', views.index_hora, name = 'index_horaria'),
    path('borrar/', views.borra_alumno, name = 'borra_alumno'),
]