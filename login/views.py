from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def login_home(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        try:
            usuario = User.objects.values('username').get(email__exact=request.POST['email'])
        except ObjectDoesNotExist:
            context = { 'msj' : 'Correo o Clave no válidos'}
            return render(request, 'login.html', context)
        except Exception as erro:
            context = { 'msj' : erro }
            return render(request, 'login.html', context)
        usuario_aut = authenticate(request, username = usuario['username'], password = request.POST['password'])
        if usuario_aut is None:
            context = { 'msj' : 'Correo o Clave no válidos'}
            return render(request, 'login.html', context)
        else:
            login(request, usuario_aut)
            return redirect('index_agenda')
    else:
        context = { 'msj' : 'Metodo desconocido, intente de nuevo por favor' }
        return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    context = { 'msj' : 'Ha cerrado correctamente la Sesión'}
    return render(request, 'login.html', context)



    
