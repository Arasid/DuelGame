from django import forms
from django.db.models import Q

from .models import GameType, Person, Duel

class AddDuelForm(forms.Form):
    game = forms.ModelChoiceField(
            queryset=GameType.objects.all(),
            widget=forms.Select(attrs={
                'class': 'form-control',
            }),
            empty_label='-- select game --',
    )
    people = Person.objects.all()
    winner = forms.ModelChoiceField(
            queryset=people,
            widget=forms.Select(attrs={
                'class': 'form-control',
                'size': len(people),
            }),
            empty_label=None,
    )
    loser = forms.ModelChoiceField(
            queryset=people,
            widget=forms.Select(attrs={
                'class': 'form-control',
                'size': len(people),
            }),
            empty_label=None,
    )

    def clean(self):
        cleaned_data = super().clean()
        winner = cleaned_data.get('winner')
        loser = cleaned_data.get('loser')
        if None in [winner, loser]:
            return

        if winner == loser:
            raise forms.ValidationError('Winner and loser cannot be the same.')
        if winner.group == loser.group:
            raise forms.ValidationError('Winner and loser are from same group.')

        last_duel_of_winner = Duel.objects.filter(Q(winner=winner) | Q(loser=winner)).last()
        last_duel_of_loser = Duel.objects.filter(Q(winner=loser) | Q(loser=loser)).last()

        if last_duel_of_winner is not None and loser in [last_duel_of_winner.winner, last_duel_of_winner.loser]:
            raise forms.ValidationError('%s had his last duel with %s.' % (winner, loser))

        if last_duel_of_loser is not None and winner in [last_duel_of_loser.winner, last_duel_of_loser.loser]:
            raise forms.ValidationError('%s had his last duel with %s.' % (loser, winner))

