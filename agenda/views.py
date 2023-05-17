from django.shortcuts import render

# Create your views here.
def index_agenda(request):
    return render(request, 'index.html')

def index_diario(request):
    return render(request, 'a_diaria.html')

def index_hora(request):
    return render(request, 'a_horaria.html')