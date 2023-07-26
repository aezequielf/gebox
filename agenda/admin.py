from django.contrib import admin
from .models import turnos, grupos, params_ag, perfil
from django.utils import timezone
from .utils.semana import genera_semana, dia_num2ab
from django.contrib.auth.models import User

class turnosAdmin(admin.ModelAdmin):
    actions = ['generar_turno_semanal']
    
    def generar_turno_semanal(self, request, queryset):
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
    
class perfilAdmin(admin.ModelAdmin):
    actions = ['desactivar_alumnos', 'activar_alumnos']

    def desactivar_alumnos(self, request, queryset):
        queryset = queryset.exclude(is_staff=True)
        for alumno in queryset:
            alumno.is_active = False
            alumno.save()
    
    def activar_alumnos(self, request, queryset):
        queryset = queryset.exclude(is_staff=True)
        for alumno in queryset:
            alumno.is_active = True
            alumno.save()
            
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions



admin.site.register(turnos, turnosAdmin)
admin.site.register(grupos)
#admin.site.unregister(User)
#admin.site.register(User, perfilAdmin)
admin.site.register(params_ag)