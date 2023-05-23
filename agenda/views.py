from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import params_ag, turnos
from .utils.semana import genera_semana, dia_num2ab
# Create your views here.

def index_agenda(request):
    return render(request, 'index.html')

def index_diario(request):
    return render(request, 'a_diaria.html')

def index_hora(request):
    return render(request, 'a_horaria.html')

def generar_semana(request):
    if request.method == 'GET':
        return render(request, 'generar_semana.html')
    elif request.method == 'POST':
        parametros = params_ag.objects.all()
        # creo un set para obtener días no repetidos desde los parametros
        param_dias = set()
        for param in parametros:
            param_dias.add(param.dia)
        # creo un diccionario para separar horarios por día
        horarioxdia = dict()
        for param_dia in param_dias:
            horarioxdia[param_dia] = parametros.filter(dia=param_dia).values('hora')
        semana_actual=genera_semana()
        #genero los turnos a partir de la semana en curso y los parámetros
        for i in range(7):
            if dia_num2ab(i) in horarioxdia:
                for j in range(len(horarioxdia[dia_num2ab(i)])):
                    turno_gen=timezone.datetime(semana_actual[i].year,semana_actual[i].month,semana_actual[i].day,horarioxdia[dia_num2ab(i)][j]['hora'].hour,horarioxdia[dia_num2ab(i)][j]['hora'].minute)
                    turno_gen=timezone.make_aware(turno_gen)
                    if len(turnos.objects.filter(dia_hora=turno_gen)) == 0:
                        turnos.objects.create(dia_hora=turno_gen)
        context = { 'msj' : '' }
        messages.success(request, '¡Proceso terminado !')
        return render(request, 'generar_semana.html', context)
    else:
        return HttpResponse('metodo desconocido')