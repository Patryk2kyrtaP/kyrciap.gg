from django.shortcuts import render, redirect
from django.http import HttpResponse

from kyrciapp.python.player_profile_info import get_summoner_info
from .forms import SummonerForm 
from django.shortcuts import render
from .forms import SummonerForm 
from kyrciapp.python.region_dictionary import choose_region
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

            # ic(request.session['summoner_name'], request.session['global_region'])
            summoner_info = get_summoner_info(request.session['summoner_name'], request.session['global_region'])
            # ic(summoner_info)
            
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
                print("Player not found.")


            puuid = summoner_info[5]  # puuid
            ic(puuid)

            chosen_summoner_info = chosen_summoner_info # + region
            print(chosen_summoner_info)
            
        # Przekierowanie do tej samej strony, aby odświeżyć informacje
        return redirect('player_info')
    else:
    # Utworzenie nowego formularza z domyślnymi wartościami z sesji
        icon = request.session.get('icon', 'default')
        ic(icon)
        summoner_name = request.session.get('summoner_name', '')
        global_region = request.session.get('global_region', '')
        form = SummonerForm(initial={'summoner_name': summoner_name, 'region': global_region})
    regions = choose_region()
    return render(request, 'player_info.html', {'form': form, 'regions': regions, 'icon': icon})
    