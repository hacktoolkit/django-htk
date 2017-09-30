from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.template import Context
from django.template import loader
from django.urls import reverse

from htk.api.utils import json_response
from htk.lib.yahoo.sports.fantasy.constants import *
from htk.lib.yahoo.sports.fantasy.utils import get_yahoo_fantasy_sports_client_for_user
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data

@login_required
def index(request):
    data = wrap_data(request)
    data['tools'] = YAHOO_SPORTS_FANTASY_TOOLS
    response = _r('htk/lib/yahoo/sports/fantasy/index.html', data)
    return response

@login_required
def get_user(request):
    user = request.user
    client = get_yahoo_fantasy_sports_client_for_user(user)
    result = client.get_user()
    response = json_response(result.json_data)
    return response

@login_required
def get_user_leagues(request):
#    data = wrap_data(request)
    user = request.user
    client = get_yahoo_fantasy_sports_client_for_user(user)
    leagues = client.get_user_leagues()
    #data['api_response'] = leagues
    response = json_response(leagues.json_data)
    
    #response = _r('htk/lib/yahoo/fantasysports/api_response.html', data)
    return response

@login_required
def get_user_leagues_players(request):
    user = request.user
    client = get_yahoo_fantasy_sports_client_for_user(user)
    players = client.get_user_leagues_players()
    response = json_response(players.json_data)
    return response

@login_required
def get_user_leagues_rosters(request):
    user = request.user
    client = get_yahoo_fantasy_sports_client_for_user(user)
    rosters = client.get_user_leagues_rosters()
    response = json_response(rosters.json_data)
    return response
