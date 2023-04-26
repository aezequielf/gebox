from django.shortcuts import render

# Create your views here.
def index_agenda(request):
    return render(request, 'index.html')
