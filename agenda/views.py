from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import turnos
from .utils.semana import dia_num2let
# Create your views here.

def index_agenda(request):
    if request.method == 'GET':
        dia_inicio_semana = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        dia_inicio_semana = datetime(dia_inicio_semana.year,dia_inicio_semana.month,dia_inicio_semana.day,0,0)
        dia_inicio_semana = timezone.make_aware(dia_inicio_semana)
        diario = turnos.objects.filter( dia_hora__gte = dia_inicio_semana).order_by('dia_hora')
        dias_activos = []
        for dia in diario:
            dia_comp= (dia_num2let(dia.dia_hora.date().weekday()),dia.dia_hora.date().strftime('%d-%m-%Y'))
            if dia_comp not in dias_activos:
                dias_activos.append(dia_comp) 
        context = { 'msj': '' , 'dias' : dias_activos}
        return render(request, 'index.html', context)
    else:
        context = {'msj': 'Metodo indefinido'}
        return render(request, 'index.html', context )

def index_diario(request, fecha = None):
   if not fecha:
       context = { 'msj': 'Error: Fecha vacia' }
       return render(request, 'a_diaria.html', context )
   dia_l = fecha.split('-')
   dia = datetime(int(dia_l[2]),int(dia_l[1]),int(dia_l[0]),0,0)
   dia = timezone.make_aware(dia)
   horarios = turnos.objects.filter(dia_hora__contains=dia.date())
   horarios_activos = []
   for hora in horarios:
       hora_local=timezone.localtime(hora.dia_hora)
       
       #print(f'Hora {hora_local.time().strftime("%H:%M")} id del turno {hora.id}')
       horarios_activos.append((hora_local.time().strftime("%H:%M"),hora.id))
   context = { 'msj': '', 'fecha' : fecha , 'dia_letras': dia_num2let(dia.weekday()) , 'horarios' : horarios_activos}
   return render(request, 'a_diaria.html', context )

def index_hora(request, id = None):
    print(id)
    return render(request, 'a_horaria.html')
