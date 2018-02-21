from django.contrib import admin

from .models import GameType, Person, Duel

class GameTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class DuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'winner', 'loser')

admin.site.register(GameType, GameTypeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Duel, DuelAdmin)
