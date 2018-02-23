from django.db import models

from game import constants

# Je asi zbytocne to mat v db, ale tak preco nie O:-)
class GameType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=200)
    group = models.IntegerField(choices=constants.Group.GROUP_CHOICES)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Duel(models.Model):
    winner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='winner')
    loser = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='loser')
    game = models.ForeignKey(GameType, on_delete=models.CASCADE)

    def __str__(self):
        return '(Duel-%s-%s-%s)' % (self.winner, self.loser, self.game)

    def __unicode__(self):
        return '(Duel-%s-%s-%s)' % (self.winner, self.loser, self.game)
