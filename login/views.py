from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def login_home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index_agenda')
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        try:
            usuario = User.objects.values('username').get(email__exact=request.POST['email'])
        except ObjectDoesNotExist:
            context = { 'msj' : ''}
            messages.warning(request, '¡Correo o Clave no válidos!')
            return render(request, 'login.html', context)
        except Exception as erro:
            context = { 'msj' : '' }
            messages.add_message(request, messages.ERROR, erro, extra_tags='danger')
            return render(request, 'login.html', context)
        usuario_aut = authenticate(request, username = usuario['username'], password = request.POST['password'])
        if usuario_aut is None:
            context = { 'msj' : ''}
            messages.warning(request, '¡Correo o Clave no válidos!')
            return render(request, 'login.html', context)
        else:
            login(request, usuario_aut)
            return redirect('index_agenda')
    else:
        context = { 'msj' : '' }
        messages.add_message(request, messages.ERROR, 'Método desconocido', extra_tags='danger')
        return render(request, 'login.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Ha cerrado sesión correctamente')
    context = { 'msj' : ''}
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
                    context = { 'msj' : '', 'last_name' : request.POST['last_name'],'first_name' : request.POST['first_name'],'email' : request.POST['email'],}
                    messages.add_message(request, messages.INFO, f"¡El alias {request.POST['username']} ya está en uso ! ", extra_tags='secondary')
                    return render(request, 'register.html', context)
                messages.success(request, 'Listo, ahora espera que te aprueben para ingresar a la app. ¡Muchas gracias!')
                return render(request, 'login.html' ,context = {'msj':''} )
            else:
                context = { 'msj' : '', 'username' : request.POST['username'],'last_name' : request.POST['last_name'],'first_name' : request.POST['first_name'],'email' : request.POST['email']}
                messages.warning(request, '¡Las claves no coinciden !')
                return render(request, 'register.html', context)
        else:
            context = { 'msj' : '', 'username' : request.POST['username'],'last_name' : request.POST['last_name'],'first_name' : request.POST['first_name']}
            messages.add_message(request, messages.INFO, f"¡La dirección de correo {request.POST['email']} no está disponible !", extra_tags='secondary')
            return render(request, 'register.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Método desconocido', extra_tags='danger')
        return render(request, 'register.html', context)
    

