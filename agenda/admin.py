from django.contrib import admin
from .models import turnos, grupos, params_ag

admin.site.register(turnos)
admin.site.register(grupos)
admin.site.register(params_ag)