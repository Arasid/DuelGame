from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request, 'game/index.html', {})

def points(request):
    return HttpResponse('Here will be points.')

def add_duel(request):
    return HttpResponse('Here it will be possible to add duels.')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/game/')
            else:
                return HttpResponse('Your account is disabled.')
        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'game/login.html', {})


@login_required(login_url='/game/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/game/')

