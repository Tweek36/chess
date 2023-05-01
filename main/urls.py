from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_player_ajax', views.add_player_ajax, name='add_player_ajax'),
    path('set_winner_ajax', views.set_winner_ajax, name='set_winner_ajax'),
    path('add_competition_ajax', views.add_competition_ajax, name='add_competition_ajax')
]