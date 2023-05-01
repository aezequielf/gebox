from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
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

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        if len(User.objects.values('username').filter(email=request.POST['email'])) == 0:
            if request.POST['password1'] == request.POST['password2']:
                try:
                   User.objects.create_user(request.POST['username'].capitalize(),request.POST['email'],request.POST['password1'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],is_active=False,date_joined=timezone.now())
                except IntegrityError:
                    context = { 'msj' : f"El alias {request.POST['username']} ya está en uso ! "}
                    return render(request, 'register.html', context)
                return render(request, 'login.html' ,context = {'msj':'Ahora espera que el Coach te apruebe para poder empezar a registrarte'} )
            else:
                context = { 'msj' : 'Las claves no coinciden'}
                return render(request, 'register.html', context)
        else:
            context = { 'msj' : f"La dirección de correo {request.POST['email']} no está disponible"}
            return render(request, 'register.html', context)
    else:
        context = { 'msj' : 'Método desconocido'}
        return render(request, 'register.html', context)
