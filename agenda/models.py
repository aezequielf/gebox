from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    peso = models.IntegerField(null = True, blank = True)


class turnos(models.Model):
    dia_hora = models.DateTimeField(null = True, blank = True)
    activo = models.BooleanField(default = True)
    detalle = models.CharField(max_length = 60, null = True, blank = True)

    def __str__(self):
        turno = timezone.localtime(self.dia_hora)
        return f' Turno {turno} '
       

class grupos(models.Model):
    turno = models.ForeignKey(turnos, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        turno = timezone.localtime(self.turno.dia_hora)
        return f'{self.user.username} - {turno}'
 
class params_ag(models.Model):
    dia=models.CharField(max_length=2)
    hora=models.TimeField()
    def __str__(self) -> str:
        if self.dia == 'lu':
            return f' Lunes {self.hora}'
        if self.dia == 'ma':
            return f' Martes {self.hora}'
        if self.dia == 'mi':
            return f' Miercoles {self.hora}'
        if self.dia == 'ju':
            return f' Jueves {self.hora}'
        if self.dia == 'vi':
            return f' Viernes {self.hora}'