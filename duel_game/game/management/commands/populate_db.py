import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import Person, GameType


class Command(BaseCommand):
    help = 'Populate DB.'

    def _populate_games(self):
        with open(Path(settings.BASE_DIR) / 'games.json', 'r') as json_file:
            games = json.loads(json_file.read())

        for game in games:
            game_obj, created = GameType.objects.update_or_create(
                id=game.pop('id'),
                defaults=game
            )

            if created:
                self.stdout.write(self.style.NOTICE(f'Created ‘{game_obj.name}’ game.'))

    def _populate_people(self):
        with open(Path(settings.BASE_DIR) / 'people.csv', 'r') as csv_file:
            people = []
            for line in csv_file:
                id, name, group = line.strip().split(',')
                people.append({
                    'id': id,
                    'name': name,
                    'group': group,
                })

        for person in people:
            person_obj, created = Person.objects.update_or_create(
                id=person['id'],
                name=person['name'],
                group=person['group']
            )

            if created:
                self.stdout.write(self.style.NOTICE(f'Created ‘{person_obj.name}’ person.'))

    def handle(self, *args, **options):
        self._populate_games()
        self._populate_people()
