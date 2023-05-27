from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import turnos, grupos
from .utils.semana import dia_num2let
# Create your views here.

def index_agenda(request):
    if request.method == 'GET':
        dia_inicio_semana = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        dia_inicio_semana = datetime(dia_inicio_semana.year,dia_inicio_semana.month,dia_inicio_semana.day,0,0)
        dia_inicio_semana = timezone.make_aware(dia_inicio_semana)
        diario = turnos.objects.filter( dia_hora__gte = dia_inicio_semana).order_by('dia_hora')
        if len(diario) == 0:
            context = { 'msj': 'No se ha generado la agenda semanal aún ...' , 'dias' :' '}
            return render(request, 'index.html', context)
        dias_activos = []
        for dia in diario:
            dia_comp= (dia_num2let(dia.dia_hora.date().weekday()),dia.dia_hora.date().strftime('%d-%m-%Y'))
            if dia_comp not in dias_activos:
                dias_activos.append(dia_comp) 
        context = { 'msj': '' , 'dias' : dias_activos}
        return render(request, 'index.html', context)
    else:
        return HttpResponseNotAllowed('<h1> Metodo no disponible</h1>')

def index_diario(request, fecha = None):
   if request.method == 'GET':
        if not fecha:
            return HttpResponseBadRequest('<h1> Faltan parametros en la solicitud </h1>')
        dia_l = fecha.split('-')
        dia = datetime(int(dia_l[2][:4]),int(dia_l[1]),int(dia_l[0]),0,0)
        dia = timezone.make_aware(dia)
        horarios = turnos.objects.filter(dia_hora__contains=dia.date())
        horarios_activos = []
        for hora in horarios:
            hora_local=timezone.localtime(hora.dia_hora)
            horarios_activos.append((hora_local.time().strftime("%H:%M"),hora.id))
        context = { 'msj': '', 'fecha' : fecha , 'dia_letras': dia_num2let(dia.weekday()) , 'horarios' : horarios_activos}
        return render(request, 'a_diaria.html', context )
   else:
       return HttpResponseNotAllowed('<h1> Metodo no disponible</h1>')

def index_hora(request, id = None):
    if not id:
        return HttpResponseBadRequest('<h1> Faltan parametros en la solicitud </h1>')
    try:
        fecha= turnos.objects.values('dia_hora').get(id=id)
    except:
        return HttpResponseBadRequest('<h1> datos de ingreso invalidos  </h1>')
    alumnos = grupos.objects.select_related('user').values('id','user__username','user__id').filter(turno_id=id)
    anotarme = True
    for alumno in alumnos:
        if alumno['user__id'] == request.user.id:
            anotarme = False
    if len(alumnos) == 0:
        context = { 'msj' : 'Nadie anotado todavía ...', 'alumnos' : alumnos, 'dia_letra' :  dia_num2let( fecha['dia_hora'].weekday()), 'dia_hora' : timezone.localtime(fecha['dia_hora']).strftime("%d-%m-%Y %H:%M") ,'id_turno': id, 'anotarme' : True  } 
    else:
        context = { 'msj' : '', 'alumnos' : alumnos, 'dia_letra' :  dia_num2let( fecha['dia_hora'].weekday()), 'dia_hora' : timezone.localtime(fecha['dia_hora']).strftime("%d-%m-%Y %H:%M") , 'id_turno': id, 'anotarme': anotarme }
    return render(request, 'a_horaria.html', context)

def borra_alumno(request):
    if request.method == 'POST' and request.POST['method_'] == 'DELETE':
        grupo_id = request.POST['item_grupo_id']
        turno_id = request.POST['id_turno']
        try:
            grupo = grupos.objects.get(id=grupo_id)
        except:
            return HttpResponseBadRequest('<h1> Consulta invalida </h1>')
        grupo.delete()
        messages.warning(request, '¡Gracias por avisarnos que no vas a poder asistir a este turno !')
        return index_hora(request, turno_id)
    else:
        return HttpResponseNotAllowed('<h1> Metodo no disponible </h1>')

def agrega_alumno(request):
    if request.method == 'POST':
        if not request.POST['id_turno'] or not request.POST['id_user']:
            return HttpResponseBadRequest('<h1> Consulta invalida </h1>')
        alumno = User.objects.get(id=request.POST['id_user'])
        turno = turnos.objects.get(id=request.POST['id_turno'])
        grupos.objects.create(turno = turno, user = alumno)
        messages.success(request, '¡Te anotaste, gracias !')
        return index_hora(request, request.POST['id_turno'])
    else:
        return HttpResponseNotAllowed('<h1> Metodo no disponible </h1>')