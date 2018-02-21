from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

from .constants import WINNER_POINTS, LOSER_POINTS
from .models import Person, GameType, Duel

def index(request):
	return render(request, 'game/index.html', {})

def points(request):
    duels = Duel.objects.all()
    wins = Duel.objects.values('game', 'winner').annotate(duels=Count('loser'))
    losses = Duel.objects.values('game', 'loser').annotate(duels=Count('winner'))
    points = {}
    games = GameType.objects.all()
    people = Person.objects.all()
    for person in people:
        points[person.id] = {}
        for game in games:
            points[person.id][game.id] = 0

    for win in wins:
        winner = win['winner']
        game = win['game']
        won_duels = win['duels']
        points[winner][game] += WINNER_POINTS * won_duels
    for loss in losses:
        loser = loss['loser']
        game = loss['game']
        lost_duels = loss['duels']
        points[loser][game] += LOSER_POINTS * lost_duels
    context_dict = {
        'points': points,
        'games': games,
        'people': people,
    }
    return render(request, 'game/points.html', context_dict)

@login_required(login_url='/game/login/')
@staff_member_required
def add_duel(request):
    if request.method == 'POST':
        game_id = request.POST.get('game-select')
        winner_id = request.POST.get('winner-select')
        loser_id = request.POST.get('loser-select')

        game = GameType.objects.get(pk=game_id)
        winner = Person.objects.get(pk=winner_id)
        loser = Person.objects.get(pk=loser_id)
        if winner == loser:
            return HttpResponseRedirect('/game/add_duel/')

        Duel.objects.create(
                winner=winner,
                loser=loser,
                game=game)

        return HttpResponseRedirect('/game/add_duel/')
    else:
        users = Person.objects.all()
        games = GameType.objects.all()

        context_dict = {
            'users': users,
            'games': games,
        }
        return render(request, 'game/add_duel.html', context_dict)

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

