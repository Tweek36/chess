from django.shortcuts import render
import string
from .models import Game, Player, Competition
from django.http import JsonResponse
import json

def index(request):
    players = Player.objects.all()
    competitions = Competition.objects.all()
    return render(request, 'main/index.html', {'competitions' : competitions, 'players' : players})

def add_player_ajax(request):
    request_dict = dict(request.POST)
    c = 0
    for i in range(0,len(request_dict['names[]'])):
        for r in range(0,int(request_dict['repeats[]'][i])):
            if request_dict['names[]'][i] == '':
                Player.objects.create_player()
            else:
                Player.objects.create_player(name=request_dict['names[]'][i])
            
            c+=1
    return JsonResponse({'players':c})

def set_winner_ajax(request):
    game = Game.objects.get(pk=request.GET['game'])
    game.set_winner(Player.objects.get(pk=request.GET['winner']))
    return JsonResponse({'ok':'ok'})

def add_competition_ajax(request):
    list_players = json.loads(request.GET.get('players'))
    print(list_players)
    competition = Competition.objects.create()
    for player in list_players:
        competition.add_player(Player.objects.get(pk=int(player)))
    competition.generate_competition()
    return JsonResponse({'ans':'true'})