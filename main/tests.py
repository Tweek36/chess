from django.test import TestCase
from .models import Player, Competition, Game

class caseTest(TestCase):
    def test_player_create(self):
        
        names = ['Bob', '$123da', '^7afda']

        new_players = []
        for name in names:
            Player.objects.create(name = name)

        self.assertEqual(Player.objects.all().count(),len(names))
    
    def test_competition_create(self):
        competition = Competition.objects.create()
        players = []
        for i in range(0, 4):
            players.append(Player.objects.create_player())
        for player in players:
            competition.add_player(player)
        self.assertEqual(competition.players.all().count(),len(players))

    def test_competition_generate_competition(self):
        competition = Competition.objects.create()
        players = []
        for i in range(0, 4):
            players.append(Player.objects.create_player())
        for player in players:
            competition.add_player(player)
        competition.generate_competition()
        self.assertEqual(competition.games.all().count(),3)