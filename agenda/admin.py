from django.contrib import admin
from .models import turnos, grupos, params_ag, perfil


class turnosAdmin(admin.ModelAdmin):
    actions = ['desactivar_turno', 'activar_turno', 'eliminar_turno']
    
    def desactivar_turno(self, request, queryset):
        for turno in queryset:
            turno.activo = False
            turno.save()
    
    def activar_turno(self, request, queryset):
        for turno in queryset:
            turno.activo = True
            turno.save()
    
    def eliminar_turno(self, request, queryset):
        for turno in queryset:
            turno.delete()
            
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# class perfilAdmin(admin.ModelAdmin):
#     actions = ['desactivar_perfil', 'activar_perfil']
    
#     def desactivar_perfil(self, request, queryset):
#         for perfil in queryset:
#             perfil.activo = False
#             perfil.save()
    
#     def activar_perfil(self, request, queryset):
#         for perfil in queryset:
#             perfil.activo = True
#             perfil.save()
            
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
        
    




admin.site.register(turnos, turnosAdmin)
admin.site.register(grupos)
# admin.site.register(perfil, perfilAdmin)
admin.site.register(params_ag)