# Django Imports
from django.conf import settings
from django.urls import include
from django.urls import re_path

# HTK Imports
import htk.lib.yahoo.sports.fantasy.views as views


urlpatterns = (
    re_path(r'^$', views.index, name='index'),
    re_path(r'^get_user$', views.get_user, name='lib_yahoo_sports_fantasy_get_user'),
    re_path(r'^get_user_leagues$', views.get_user_leagues, name='lib_yahoo_sports_fantasy_get_user_leagues'),
    re_path(r'^get_user_leagues_players$', views.get_user_leagues_players, name='lib_yahoo_sports_fantasy_get_user_leagues_players'),
    re_path(r'^get_user_leagues_rosters$', views.get_user_leagues_rosters, name='lib_yahoo_sports_fantasy_get_user_leagues_rosters'),
)
