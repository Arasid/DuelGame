from django import forms

from .models import GameType, Person

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
        if winner is not None and winner == loser:
            raise forms.ValidationError('Winner and loser cannot be the same.')
        if None not in [winner, loser] and winner.group == loser.group:
            raise forms.ValidationError('Winner and loser are from same group.')
