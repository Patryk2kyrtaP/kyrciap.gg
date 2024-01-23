from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from flask import request

from kyrciapp.python.player_profile_info import get_maestry_points, get_rank_info, get_summoner_info
from kyrciapp.python.region_dictionary import choose_region
from kyrciapp.python.match_info import get_match_id
from .forms import SummonerForm 
from django.shortcuts import render
from .forms import SummonerForm 
import logging
from icecream import ic

logger = logging.getLogger(__name__)

def index(request):

    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            global_region = form.cleaned_data['region']
            logger.info(f"Summoner Name: {summoner_name}, Region: {global_region}")
            request.session['summoner_name'] = summoner_name
            request.session['global_region'] = global_region
            
            return redirect('player_info')
    else:
        form = SummonerForm()
    
    regions = choose_region()
    return render(request, 'index.html', {'form': form, 'regions': regions})

def player_info(request):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            request.session['summoner_name'] = form.cleaned_data['summoner_name']
            request.session['global_region'] = form.cleaned_data['region']
            return redirect('player_info')

    summoner_name = request.session.get('summoner_name', '')
    global_region = request.session.get('global_region', '')

    form = SummonerForm(initial={'summoner_name': summoner_name, 'region': global_region})

    if summoner_name and global_region:
        summoner_info = get_summoner_info(summoner_name, global_region)
        if summoner_info:
            request.session['icon'] = str(summoner_info[1])
            request.session['lvl'] = summoner_info[6]
            request.session['puuid'] = summoner_info[5]
            request.session['id'] = summoner_info[4]
            rendered_maestry = maestry_render(request)
            solo_rank_info, flex_rank_info = rank_info_render(request)
            match_ids = render_match_id(request)
            
            if solo_rank_info is None:
                solo_rank_info = {}  # Pusty słownik dla unranked

            if flex_rank_info is None:
                flex_rank_info = {}  # Pusty słownik dla unranked

            ic(solo_rank_info, flex_rank_info)
            ic(match_ids)
        else:
            rendered_maestry = []   
    else:
        rendered_maestry = []
        
    regions = choose_region()
    return render(request, 'player_info.html', {
        'form': form,
        'regions': regions,
        'icon': request.session.get('icon', 'default'),
        'player_maestry_points': rendered_maestry,
        'lvl': request.session.get('lvl', ''),
        'id': request.session.get('id', ''),
        
        'solo_rank_info': solo_rank_info,
        'flex_rank_info': flex_rank_info,
        
        'match_id': match_ids,
        
        'summoner_name': summoner_name,
        'global_region': global_region
    })

def maestry_render(request):
    puuid = request.session['puuid']
    global_region = request.session['global_region']            
    
    maestry_points = get_maestry_points(puuid, global_region)
    ic(maestry_points)
    if not maestry_points:
        return []

    rendered_maestry = []
    for maestry in maestry_points:
        rendered_maestry.append({
            'chest_granted': maestry[0],
            'champion_name': maestry[1],
            'last_play_date': maestry[2],
            'champion_level': maestry[3],
            'champion_points': maestry[4]
        })

    return rendered_maestry

def rank_info_render(request):
    encrypted_summoner_id = request.session['id']
    global_region = request.session['global_region']

    solo_q_info, flex_info = get_rank_info(encrypted_summoner_id, global_region)

    # ic(solo_q_info, flex_info)

    return solo_q_info, flex_info

def render_match_id(request):
    puuid = request.session['puuid']
    global_region = request.session['global_region']  
    
    match_ids = get_match_id(puuid, global_region, 20)
    # ic(match_ids)
    
    if not match_ids:
        return []
    
    # rendered_match_ids = []
    # for match in match_ids:
    #     rendered_match_ids.append({
    #         'match_id': match_ids[0],
    #     })
    
    return match_ids
    return rendered_match_ids