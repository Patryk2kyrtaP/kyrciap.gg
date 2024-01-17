from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from flask import request

from kyrciapp.python.player_profile_info import get_maestry_points, get_summoner_info
from kyrciapp.python.region_dictionary import choose_region
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
            global_region = request.session['global_region']
            # ic(request.session['summoner_name'], request.session['global_region'])
            summoner_info = get_summoner_info(request.session['summoner_name'], request.session['global_region'])
            ic(summoner_info)
            
            
            chosen_summoner_info = []
            region = []
            region_from_dict = str
            encrypted_summoner_id = str
            count = 20

            if summoner_info:
                request.session['icon'] = str(summoner_info[1]) 
                encrypted_summoner_id = summoner_info[4]
                ic(encrypted_summoner_id)   
                chosen_summoner_info = [summoner_info[1], summoner_info[2], 
                                        summoner_info[3], summoner_info[6],]
            else:
                raise Http404("This player does not exist in {}".format(global_region))

            lvl = chosen_summoner_info[3]
            request.session['lvl'] = lvl
            
            puuid = summoner_info[5]  # puuid
            request.session['puuid'] = puuid
            ic(puuid)

            chosen_summoner_info = chosen_summoner_info # + region
            print(chosen_summoner_info)
            return redirect('player_info')   
        # Przekierowanie do tej samej strony, aby odświeżyć informacje
    else:
    # Utworzenie nowego formularza z domyślnymi wartościami z sesji
        summoner_name = request.session.get('summoner_name', '')
        global_region = request.session.get('global_region', '')
        icon = request.session.get('icon', 'default')
        ic(icon)
        form = SummonerForm(initial={'summoner_name': summoner_name, 'region': global_region})
    
    puuid = request.session.get('puuid', '')
    summoner_name = request.session.get('summoner_name', '')
    ic(summoner_name)
    global_region = request.session.get('global_region', '')

    lvl  = request.session.get('lvl', '')
    ic(lvl)
    regions = choose_region()
    
    rendered_maestry = maestry_render(request) if puuid and global_region else []
    return render(request, 'player_info.html', {
        'form': form,
        'regions': regions,
        'icon': icon,
        'player_maestry_points': rendered_maestry,  # Przekazanie wyników funkcji do szablonu
        'lvl': lvl,
        'summoner_name': summoner_name,
        'global_region': global_region
    })
    
    # return render(request, 'player_info.html', {'form': form, 'regions': regions, 'icon': icon})
   
def maestry_render(request):
    puuid = request.session['puuid']
    global_region = request.session['global_region']            
    
    maestry_points = get_maestry_points(puuid, global_region)
    ic(maestry_points)
    if not maestry_points:
        return []

    rendered_maestry = []
    for maestry in maestry_points:
        # Przykład struktury: [chestGranted, champion_name, last_play_date, champion_level, champion_points]
        rendered_maestry.append({
            'chest_granted': maestry[0],
            'champion_name': maestry[1],
            'last_play_date': maestry[2],
            'champion_level': maestry[3],
            'champion_points': maestry[4]
        })

    return rendered_maestry
