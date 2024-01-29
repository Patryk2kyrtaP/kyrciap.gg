from cgitb import text
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from kyrciapp.python.champion_dictionary import champ_dictionary_by_name

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


from kyrciapp.python.player_profile_info import get_maestry_points, get_rank_info, get_summoner_info
from kyrciapp.python.region_dictionary import choose_region
from kyrciapp.python.match_info import get_general_match_info_by_id, get_match_id, get_match_info_by_id, loop_through_matches, player_to_loop, process_looped_info
from kyrciapp.python.champion_dictionary import champ_dictionary
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
            match_ids_count = len(match_ids)
            match_infos = render_get_general_match_info_by_id(request) if match_ids else []
            # ic(match_infos)
            
            match_detailed_infos = render_get_match_info_by_id(request) if match_ids else []
            # ic(match_detailed_infos)
            
            
            matches_with_teams = []
            for i in range(0, len(match_detailed_infos), 10):
                match_players = match_detailed_infos[i:i+10]
                if len(match_players) == 10:
                    team_1_data = []
                    team_2_data = []

                    for index, player in enumerate(match_players):
                        player_data = {
                            'name': player['summoner_name'] if player['summoner_name'] else 'Bambik',
                            'champion_icon_url': f"https://raw.communitydragon.org/latest/game/assets/characters/{player['champion_name'].lower()}/hud/{player['champion_name'].lower()}_circle_1.png",
                            'champion_name': player['champion_name']
                        }

                        if index < 5:
                            team_1_data.append(player_data)
                        else:
                            team_2_data.append(player_data)

                    matches_with_teams.append({
                        'match_id': i // 10 + 1,
                        'team_1': team_1_data,
                        'team_2': team_2_data
                    })
            
            # ic(matches_with_teams)
            my_player = []
            for i in range(0, len(match_detailed_infos), 10):
                match_players = match_detailed_infos[i:i+10]
                if len(match_players) == 10:
                    player_1 = []
                    for player in match_players[:10]:
                        if player['summoner_name'] == summoner_name:
                            champion_name = champ_dictionary_by_name(player['champion_name'])
                            champion_lvl = player['champ_level']
                            summoner1Id = player['summoner1Id']
                            summoner2Id = player['summoner2Id']
                            kills = player['kills']
                            deaths = player['deaths']
                            assists = player['assists']
                            kda_ratio = player['kda_ratio']
                            total_minions_killed = player['total_minions_killed']
                            minions_killed_min = player['minions_killed_min']
                            vision_score = player['vision_score']
                            win = player['win']
                            items_in_match = player['items_in_match']
                            
                    my_player.append({
                        'match_id': i // 10 + 1,
                        'champion_name': champion_name,
                        'champion_lvl': champion_lvl,
                        'summoner1Id': summoner1Id,
                        'summoner2Id': summoner2Id,
                        'kills': kills,
                        'deaths': deaths,
                        'assists': assists,
                        'kda_ratio': kda_ratio,
                        'total_minions_killed': total_minions_killed,
                        'minions_killed_min': minions_killed_min,
                        'vision_score': vision_score,
                        'win': win,
                        'items_in_match': items_in_match
                    })

            
            
            processed_looped_info = render_loop_info(request)
            
            ic(processed_looped_info)
            
            # ic(match_detailed_infos)

            
            if solo_rank_info is None:
                solo_rank_info = {}  # Pusty słownik dla unranked

            if flex_rank_info is None:
                flex_rank_info = {}  # Pusty słownik dla unranked

            # ic(solo_rank_info, flex_rank_info)
            # ic(match_ids)
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
        'match_ids_count': match_ids_count,
        
        'match_infos': match_infos,
        
        'match_detailed_infos': match_detailed_infos,
        
        'matches_with_teams': matches_with_teams, 
        
        'my_player': my_player,
        
        'processed_looped_info': processed_looped_info,
        
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

    ic(solo_q_info, flex_info)

    return solo_q_info, flex_info

def render_match_id(request):
    puuid = request.session['puuid']
    global_region = request.session['global_region']  
    
    match_ids = get_match_id(puuid, global_region, 3) #LICZBA GIER DO ZMIANY
    request.session['match_ids'] = match_ids 
    # ic(request.session['match_ids'])
    
    if not match_ids:
        return []

    return match_ids

def render_get_general_match_info_by_id(request):
    global_region = request.session['global_region']  
    match_ids = request.session['match_ids']
    ic(match_ids)
    
    i = 0
    rendered_match_info = []
    for match_id in match_ids:
        match_info = get_general_match_info_by_id(match_id, global_region)
        if match_info:
            i = i + 1
            rendered_match_info.append({
                'match_id': i,
                'game_duration': match_info[0],
                'game_mode': match_info[1],
                'game_type': match_info[2],
                'game_version': match_info[3],
                'platform_Id': match_info[4],
                'when_form_today': match_info[5],
                'queue_name': match_info[6]
            })

    ic(rendered_match_info)    
    
    return rendered_match_info

def render_get_match_info_by_id(request):
    global_region = request.session['global_region']
    match_ids = request.session['match_ids']

    i = 0
    rendered_match_details = []
    for match_id in match_ids:
        match_details = get_match_info_by_id(match_id, global_region)
        i = i + 1
        if match_details:
            for player_detail in match_details:
                rendered_match_details.append({
                    'match_id': i,
                    'summoner_name': player_detail[0],
                    'champion_name': player_detail[1],
                    'champ_level': player_detail[2],
                    'kills': player_detail[3],
                    'deaths': player_detail[4],
                    'assists': player_detail[5],
                    'kda_ratio': player_detail[6], 
                    'total_minions_killed': player_detail[7],
                    'minions_killed_min': player_detail[8],
                    'vision_score': player_detail[9], 
                    'role': player_detail[10],
                    'lane': player_detail[11],
                    'summoner1Id': player_detail[12],
                    'summoner2Id': player_detail[13],
                    'longest_time_spent_living': player_detail[14],
                    'win': player_detail[15],
                    'largest_multi_kill': player_detail[16],
                    'penta_kills': player_detail[17],
                    'total_damage_dealt': player_detail[18],
                    'gold_earned': player_detail[19],
                    'first_Blood_Kill': player_detail[20],
                    'items_in_match': player_detail[21],
                    # Dodaj pozostałe pola w podobny sposób
                    'runes': player_detail[-1]  # Zakładając, że runy są ostatnim elementem w player_detail
                })

    return rendered_match_details


def render_loop_info(request):
    global_region = request.session['global_region']
    match_ids = request.session['match_ids']
    puuid = request.session['puuid']

    looped_info = []

    for match_id in match_ids:
        match_data = loop_through_matches(match_id, global_region)
        # ic(match_data)
        looped_info.append(player_to_loop(puuid, match_data))


    processed_looped_info = process_looped_info(looped_info)
    
    return processed_looped_info


# ================================================================================================
def signup_view(request):
    
    regions = choose_region()


    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            password_confirmation = form.cleaned_data.get('password2')
            region = form.cleaned_data.get['region']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'regions': regions})


def custom_login_view(request):
    return LoginView.as_view(template_name='login.html')(request)