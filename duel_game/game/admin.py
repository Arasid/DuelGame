from django.contrib import admin

from .models import GameType, Person, Duel

class GameTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')

class DuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'game', 'winner', 'loser')

admin.site.register(GameType, GameTypeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Duel, DuelAdmin)
