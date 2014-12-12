from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

import htk.lib.yahoo.sports.fantasy.views as views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^get_user$', views.get_user, name='lib_yahoo_sports_fantasy_get_user'),
    url(r'^get_user_leagues$', views.get_user_leagues, name='lib_yahoo_sports_fantasy_get_user_leagues'),
    url(r'^get_user_leagues_players$', views.get_user_leagues_players, name='lib_yahoo_sports_fantasy_get_user_leagues_players'),
    url(r'^get_user_leagues_rosters$', views.get_user_leagues_rosters, name='lib_yahoo_sports_fantasy_get_user_leagues_rosters'),
)
