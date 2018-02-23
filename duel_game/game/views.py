from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

from game import constants
from .constants import WINNER_POINTS, LOSER_POINTS
from .forms import AddDuelForm
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
        points[winner][game] += constants.WINNER_POINTS * won_duels
    for loss in losses:
        loser = loss['loser']
        game = loss['game']
        lost_duels = loss['duels']
        points[loser][game] += constants.LOSER_POINTS * lost_duels

    for person in people:
        product = 1
        for game in games:
            product *= points[person.id][game.id]
        points[person.id]['product'] = product

    people = sorted(people, key=lambda person : -points[person.id]['product'])

    last_points = -1
    last_order = 0
    for person in people:
        if points[person.id]['product'] != last_points:
            last_order += 1
            last_points = points[person.id]['product']
        points[person.id]['order'] = last_order

    groups = constants.Group.GROUP_CHOICES

    context_dict = {
        'points': points,
        'games': games,
        'people': people,
        'groups': groups,
    }
    return render(request, 'game/points.html', context_dict)

@login_required
@staff_member_required
def add_duel(request):
    if request.method == 'POST':
        form = AddDuelForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data.get('game')
            winner = form.cleaned_data.get('winner')
            loser = form.cleaned_data.get('loser')

            request.session['game_type'] = game.id

            Duel.objects.create(
                    winner=winner,
                    loser=loser,
                    game=game)

            return redirect('add_duel')
    else:
        if request.session.get('game_type', 0):
            form = AddDuelForm(initial={'game': request.session.get('game_type')})
        else:
            form = AddDuelForm()
    people = Person.objects.all()
    people_groups = {}
    for person in people:
        people_groups[person.id] = person.group

    context_dict = {
        'form': form,
        'people_groups': people_groups,
    }
    return render(request, 'game/add_duel.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

