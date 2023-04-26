from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index_agenda, name='index_agenda'),
]