from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    peso = models.IntegerField(null = True, blank = True)

class turnos(models.Model):
    dia_hora = models.DateTimeField(null = True, blank = True)
    activo = models.BooleanField(default = True)
    detalle = models.CharField(max_length = 60, null = True, blank = True)
    def __str__(self):
        return f' Turno {self.dia_hora} '

class grupos(models.Model):
    turno = models.ForeignKey(turnos, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return f'{self.user.username} - {self.turno.dia_hora}'
 
