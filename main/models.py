from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import math

class PlayerManager(models.Manager):
    use_in_migrations = True

    __NAMES = ['Aaron', 'Adam', 'Addison', 'Aden', 'Adrian', 'Alexander', 'Andrew', 'Asher', 'Ashton', 'Austin', 'Avery', 'Benjamin', 'Bennett', 'Bentley', 'Blake', 'Brayden', 'Brody', 'Cameron', 'Carson', 'Carter', 'Charles', 'Chase', 'Collin', 'Colton', 'Connor', 'Cooper', 'Daniel', 'Declan', 'Dillan', 'Dominic', 'Eli', 'Elijah', 'Elliot', 'Emmett', 'Ethan', 'Evan', 'Finn', 'Gabriel', 'Gage', 'Gavin', 'Grayson', 'Harper', 'Hayden', 'Henry', 'Holden', 'Hudson', 'Hunter', 'Ian', 'Isaac', 'Isaiah', 'Jack', 'Jackson', 'Jacob', 'Jaden', 'James', 'Jasper', 'John', 'Jonah', 'Joseph', 'Joshua', 'Jude', 'Julian', 'Kaleb', 'Kayden', 'Kole', 'Landen', 'Levi', 'Liam', 'Logan', 'Lucas', 'Luke', 'Mason', 'Matthew', 'Max', 'Micah', 'Michael', 'Miles', 'Nathan', 'Nathaniel', 'Nicholas', 'Noah', 'Nolan', 'Oliver', 'Owen', 'Parker', 'Quinn', 'Riley', 'Ryan', 'Ryder', 'Samuel', 'Sawyer', 'Sebastian', 'Seth', 'Thomas', 'Tristen', 'Tyler', 'William', 'Wyatt', 'Xavier', 'Zackery', 'Abigail', 'Adalyn', 'Addison', 'Adelaide', 'Alexa', 'Alexis', 'Alice', 'Alissa', 'Amelia', 'Ana', 'Annabelle', 'Aria', 'Arianna', 'Aubrey', 'Audrey', 'Aurora', 'Autumn', 'Ava', 'Bailey', 'Bella', 'Brooke', 'Brooklyn', 'Cadence', 'Caroline', 'Charlotte', 'Chloe', 'Claire', 'Clara', 'Delilah', 'Eden', 'Eleanor', 'Elisabeth', 'Ella', 'Emily', 'Emma', 'Esme', 'Eva', 'Evangeline', 'Evelyn', 'Fiona', 'Gabriella', 'Gabrielle', 'Genevieve', 'Grace', 'Hannah', 'Harper', 'Hayden', 'Hayley', 'Isabel', 'Isabella', 'Isla', 'Julia', 'Juliet', 'Katherine', 'Kira', 'Lauren', 'Leah', 'Leila', 'Lila', 'Lillian', 'Lily', 'Lorelei', 'Lucy', 'Lydia', 'Mackenzie', 'Madeline', 'Madison', 'Mia', 'Molly', 'Morgan', 'Natalie', 'Norah', 'Olivia', 'Paige', 'Payton', 'Penelope', 'Peyton', 'Piper', 'Quinn', 'Reagan', 'Riley', 'Rosalie', 'Ruby', 'Sadie', 'Samantha', 'Savanna', 'Scarlett', 'Sienna', 'Sophia', 'Sophie', 'Stella', 'Sydney', 'Taylor', 'Teagan', 'Victoria', 'Violet', 'Vivienne', 'Willow', 'Zoe', 'Zoey']

    def create_player(self, name=None):
        if name is None:
            name = self.__NAMES[random.randint(0, len(self.__NAMES)-1)]
        player = self.model(name=name)
        player.save(using=self._db)
        return player

class Player(models.Model):
    name = models.CharField(_("Name"), max_length=32)

    objects = PlayerManager()

    def __str__(self) -> str:
        return self.name

class GameManager(models.Manager):
    use_in_migrations = True

    def create_game(self, winner=None, next_game=None, level=1):
        game = self.model(winner=winner, next_game=next_game, level=level)
        game.save(using=self._db)
        return game
        

class Game(models.Model):
    players = models.ManyToManyField(Player, related_name='+', blank=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    next_game = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(default=0)

    objects = GameManager()

    def __str__(self) -> str:
        if len(self.players.all()) == 2:
            return self.players.all()[0].name + " vs " + self.players.all()[1].name
        else:
            return "Game: " + str(self.id)
        
    def add_player(self, player):
        self.players.add(player)
        return self
    
    def get_winner(self):
        return self.winner
    
    def get_level(self):
        return self.level
    
    def get_next_game(self):
        return self.next_game
    
    def set_winner(self, w):
        self.winner = w
        if self.next_game is not None:
            self.next_game.add_player(w)
        self.save()
        return self
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def generate_winner(self):
        rnd = random.randint(0,1)
        return self.set_winner(self.players.all()[rnd])
    
class CompetitionManager(models.Manager):
    use_in_migrations = True

    def create_competition(self):
        c = self.model()
        c.save(using=self._db)
        return c
    
class Competition(models.Model):
    players = models.ManyToManyField(Player, blank=True)
    games = models.ManyToManyField(Game, blank=True)
    level = models.IntegerField(blank=True, default=1)

    objects = CompetitionManager()

    def __str__(self) -> str:
        return "Competition: " + str(self.id)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_winner(self):
        return self.games[-1].get_winner()
    
    def add_player(self, player):
        self.players.add(player)
        return self
    
    def add_game(self, game):
        self.games.add(game)
        return self
    
    def generate_competition(self, level=None, game=None, players=None):
        if players is None:
            players = set(self.players.all())
        if level is None:
            level = math.log2(len(players))
            self.level = level
        if game is None:
            game = Game.objects.create_game(level=level)
            self.add_game(game)
        if level == 1:
            player1 = players.pop()
            player2 = players.pop()
            game.add_player(player1).add_player(player2)
        else:
            previous_game1 = Game.objects.create_game(level=level-1, next_game=game)
            self.add_game(previous_game1)
            self.generate_competition(level=level-1, game=previous_game1, players=players)
            previous_game2 = Game.objects.create_game(level=level-1, next_game=game)
            self.add_game(previous_game2)
            self.generate_competition(level=level-1, game=previous_game2, players=players)

