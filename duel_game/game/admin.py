from django.contrib import admin

from .models import GameType, Person, Duel

admin.site.register(GameType)
admin.site.register(Person)
admin.site.register(Duel)
