from cgitb import text
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import FollowedSummoner
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from .forms import SignUpForm
from .forms import SummonerForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

from kyrciapp.python.champion_dictionary import champ_dictionary_by_name, champ_dictionary_by_name2
from kyrciapp.python.player_profile_info import check_summoner_exists, get_maestry_points, get_rank_info, get_summoner_info
from kyrciapp.python.region_dictionary import choose_region
from kyrciapp.python.match_info import get_general_match_info_by_id, get_match_id, get_match_info_by_id, loop_through_matches, player_to_loop, process_looped_info

from icecream import ic
import logging

from email.message import EmailMessage
import ssl
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPException, SMTPServerDisconnected
import os

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


    if check_summoner_exists(summoner_name, global_region) == True:

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

                    champion_name = None
                    champion_lvl = None
                    summoner1Id = None
                    summoner2Id = None
                    kills = None
                    deaths = None
                    assists = None
                    kda_ratio = None
                    total_minions_killed = None
                    minions_killed_min = None
                    vision_score = None
                    win = None
                    items_in_match = None

                    # ic(match_players)
                    if len(match_players) == 10:
                        for player in match_players[:10]:
                            if player['summoner_name'] == summoner_name:
                                ic(player['champion_name'])
                                champion_name =     champ_dictionary_by_name(player['champion_name'])
                                ic(champion_name)
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
    
    else: 
        messages.error(request, f"Summoner {summoner_name} does not exist in region {global_region}.")
        return redirect('index')
        
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

    # ic(solo_q_info, flex_info)

    return solo_q_info, flex_info

def render_match_id(request):
    puuid = request.session['puuid']
    global_region = request.session['global_region']  
    
    match_ids = get_match_id(puuid, global_region, 2) #LICZBA GIER DO ZMIANY
    request.session['match_ids'] = match_ids 
    # ic(request.session['match_ids'])
    
    if not match_ids:
        return []

    return match_ids

def render_get_general_match_info_by_id(request):
    global_region = request.session['global_region']  
    match_ids = request.session['match_ids']
    # ic(match_ids)
    
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
                'queue_name': match_info[6],
                'get_id': match_id,
            })

    ic(rendered_match_info)    
    
    return rendered_match_info

def render_get_match_info_by_id(request):
    global_region = request.session['global_region']
    match_ids = request.session['match_ids']

    i = 0
    rendered_match_details = []
    for match_id in match_ids:
        # ic(match_id)
        match_details = get_match_info_by_id(match_id, global_region)
        i = i + 1
        # ic(match_details)
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



# =====================================================================================================
def player_info_view(request, summoner_name, region):
    # Tutaj logika pobierania danych gracza na podstawie summoner_name i region
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            return redirect('player_info')
    
    if summoner_name and region:    
        summoner_info = get_summoner_info(summoner_name, region)

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
        # 'form': form,
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
        'global_region': region
    })

# =====================================================================================================


def signup_view(request):
    regions = choose_region()
    
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form, 'regions': regions})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Incorrect username or password'})

    return render(request, 'login.html')

# =====================================================================================================

def follow_summoner_view(request):

    if request.method == 'POST':
        summoner_name = request.POST.get('summoner_name')
        region = request.POST.get('region')

        if check_summoner_exists(summoner_name, region) == True:
        # Utworzenie nowego obiektu FollowedSummoner i zapisanie go
            if FollowedSummoner.objects.filter(user=request.user, name=summoner_name, region=region).exists():
                message = f"Player {summoner_name} is already followed."
                followed_summoners = FollowedSummoner.objects.filter(user=request.user)
                regions = choose_region()
                context = {
                    'error_message': message,
                    'regions': regions,
                    'followed_summoners': followed_summoners,
                }
                return render(request, 'profile.html', context)

            # Gracz nie jest jeszcze obserwowany, więc dodajemy go
            followed_summoner = FollowedSummoner(user=request.user, name=summoner_name, region=region)
            followed_summoner.save()

        else:          
            messages.error(request, f"Summoner {summoner_name} does not exist in region {region}.")
        
        return redirect('profile')

    return render(request, 'index.html')

def unfollow_summoner_view(request, summoner_id):
    summoner = get_object_or_404(FollowedSummoner, id=summoner_id, user=request.user)
    summoner.delete()
    return redirect('profile')

def profile_view(request):
    regions = choose_region()
    followed_summoners = FollowedSummoner.objects.filter(user=request.user)
    
    
    
    for summoner in followed_summoners:
        summoner_info = get_summoner_info(summoner.name, summoner.region)
        if summoner_info:
            # name_region = summoner.name + summoner.region
            # # ic(name_region)
            # length = len(name_region)
            # # ic(length)
            # set_length = 20
            # length_dif = set_length - length
            # # ic(length_dif)
            # summoner.spaces = "a" * length_dif
            # ic(summoner.spaces)
            request.session['id'] = summoner_info[4]
            request.session['global_region'] = summoner.region
            solo_rank_info, flex_rank_info = rank_info_render(request)
            # ic(solo_rank_info)
            # ic(flex_rank_info)
    #         # Dodanie informacji o randze do obiektu summoner
            summoner.solo_rank_info = solo_rank_info if solo_rank_info else {}
            summoner.flex_rank_info = flex_rank_info if flex_rank_info else {}
    
    


    context = {    
        'regions': regions,
        'followed_summoners': followed_summoners
    }
    return render(request, 'profile.html', context)
# =====================================================================================================

def logout_view(request):
    logout(request)
    return redirect('index')

def logout_confirm_view(request):
    # Strona potwierdzenia wylogowania
    return render(request, 'logout_confirm.html')

@require_POST
def confirm_logout(request):
    # Wylogowanie użytkownika
    logout(request)
    return HttpResponseRedirect('/')

def champions_view(request):
    champions_dict = champ_dictionary_by_name2()  # Wywołanie funkcji, aby uzyskać słownik
    context = {
        'champions': champions_dict
    }
    ic(context)
    return render(request, 'champions.html', context)

def contact_view(request):

    email_sender = 'kyrciap.gg@gmail.com'
    email_password = os.environ.get('EMAIL_PASSWORD') 
    ic(email_password)
    email_reciver = 'kyrciap.gg@gmail.com'

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_reciver
            em['Subject'] = subject

            context = ssl.create_default_context()

            full_message = f"Received message below from {name}, \n\n Email: {email}, \n\n {message}"
            em.set_content(full_message)
            
            
            with SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_reciver, em.as_string())         # Użyj send_message zamiast sendmail i em.as_string()
            messages.success(request, "Message sent successfully")
        except Exception as e:
            messages.error(request, "There was a problem while sending your message, try again later")
            ic(e)
            
        return redirect('contact') 
    else:
        return render(request, 'contact.html')
    
def detailed_match_info_view(request, match_ids):

    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            request.session['summoner_name'] = form.cleaned_data['summoner_name']
            request.session['global_region'] = form.cleaned_data['region']
            return redirect('player_info')

    # ic(match_ids)
    regions = choose_region()
    
    
    
    global_region = request.session.get('global_region')
    ic(global_region)
    match_details = get_match_info_by_id(match_ids, global_region)
    # ic(match_details)
    rendered_match_details = []
    if match_details:
        i = 1  # Zakładamy, że mamy do czynienia z jednym meczem, więc indeks i jest stały
        for player_detail in match_details:
            champion_id = champ_dictionary_by_name(player_detail[1])
            ic(champion_id)
            rendered_match_details.append({
                'match_ids': match_ids,
                'summoner_name': player_detail[0],
                'champion_name': champion_id,       #player_detail[1],
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
        
    context = {
        'detailed_match_info': rendered_match_details,
        'regions': regions
    }
    return render(request, 'detailed_match_info.html', context)