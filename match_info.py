import datetime
import requests
from icecream import ic
from collections import Counter
from statistics import mean

from kyrciapgg.kyrciapp.python.config import get_api_key, setup_cassiopeia
from item_dictionary import item_dictionary
from player_profile_info import get_game_name_by_puuid
from region_dictionary import global_region_dictionary, region_dictionary
from summoner_spell_dictionary import summoner_spells_dictionary
from cassiopeia import Rune
from region_dictionary import region_dictionary
from queue_dictionary import queue_dictionary


def get_match_id(puuid, global_region, count):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    global_region2 = global_region_dictionary(global_region)
    api_url_match_v5_by_puuid = f'https://{global_region2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}'
    api_url = api_url_match_v5_by_puuid + '&api_key=' + api_key

    try:
        resp = requests.get(api_url)
        print("Status Code:", resp.status_code)
        if resp.status_code == 200:
            match_id = resp.json()
            print(match_id)
            return match_id
        
        else:
            print("Error in the API request")
    except Exception as e:
        print("Error occurred:", e)

def get_general_match_info_by_id(match_id, global_region):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    global_region2 = global_region_dictionary(global_region)
    api_url_match_info = f'https://{global_region2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    api_url = api_url_match_info + '?api_key=' + api_key

    try:
        resp = requests.get(api_url)
        print("Status Code:", resp.status_code)
        if resp.status_code == 200:
            match_info = resp.json()
            #match_info.keys()
            
            game_duration = match_info['info']['gameDuration']
            game_duration = minutes, seconds_remainder = divmod(game_duration, 60) #Converts seconds to minutes
            
            game_mode = match_info['info']['gameMode']
            # game_name = match_info['info']['gameName']
            game_type = match_info['info']['gameType']
            game_version = match_info['info']['gameVersion']
            platform_Id = match_info['info']['platformId']
            platform_Id = region_dictionary(platform_Id)
            game_creation = match_info['info']['gameCreation']
            queue_id = match_info['info']['queueId']
            queue_name = queue_dictionary(queue_id)
            # ic(queue_name)
        
            # Obliczenie daty kiedy rozegrano grę,
            # obliczenie ile dni minęło od tego czasu
            game_creation_seconds = game_creation / 1000.0
            formatted_game_creation = datetime.datetime.fromtimestamp(game_creation_seconds)
            today = datetime.datetime.now()
            when_form_today = today - formatted_game_creation
            when_form_today = when_form_today.days
            
            # queue_id =  match_info['info']['queueId']
            general_match_info = [game_duration,
                                  game_mode,
                                  game_type,
                                  game_version,
                                  platform_Id,
                                  when_form_today,
                                  queue_name
                                  ]
            
            # ic(platform_Id)
            return general_match_info
        
        else:
            print("Error in the API request")
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None     
 
def get_match_info_by_id(match_id, global_region):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    global_region2 = global_region_dictionary(global_region)
    api_url_match_info = f'https://{global_region2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    api_url = api_url_match_info + '?api_key=' + api_key

    setup_cassiopeia()
    
    
    try:
        resp = requests.get(api_url)
        print("Status Code:", resp.status_code)
        if resp.status_code == 200:
            match_info = resp.json() 
    
            all_players_info = []
            game_duration = match_info['info']['gameDuration']
            region_from_dict = region_dictionary(match_info['info']['platformId'])
            # print(f'GameDuration: {game_duration}')           
            
            players_in_match = match_info['info']['participants'][:10]
            for player in players_in_match:
                
                summoner_name = player['summonerName']  #Y
                champion_name = player['championName']  #Y
                champ_level = player['champLevel']      #Y
                kills = player['kills']                 #Y
                deaths = player['deaths']               #Y
                assists = player['assists']             #Y
                
                if deaths != 0:
                    kda_ratio = round((kills + assists) / deaths, 2)  #Y
                else:
                    if deaths == 0:
                        kda_ratio = round((kills + assists), 2)
                
                total_minions_killed = player['totalMinionsKilled']
                minions_killed_min = round(total_minions_killed/(game_duration/60), 1)
                vision_score = player['visionScore']
                gold_earned = player['goldEarned']
                first_Blood_Kill = player['firstBloodKill']
                items_in_match = [item_dictionary(player['item0']), item_dictionary(player['item1']), #Y
                                  item_dictionary(player['item2']), item_dictionary(player['item3']),
                                  item_dictionary(player['item4']), item_dictionary(player['item5']),
                                  item_dictionary(player['item6'])]
                
                role = player['role']
                lane = player['lane']
                # summoner1Id = summoner_spells_dictionary(player['summoner1Id'])
                # summoner2Id = summoner_spells_dictionary(player['summoner2Id'])
                
                summoner1Id = (player['summoner1Id'])
                summoner2Id = (player['summoner2Id'])
                
                longest_time_spent_living = int((player['longestTimeSpentLiving'])/60)
                win = player['win']
                largest_multi_kill = player['largestMultiKill']
                penta_kills = player['pentaKills']
                total_damage_dealt = player['totalDamageDealt']
                

                player_info = [summoner_name, champion_name, champ_level, kills, deaths, assists, 
                               kda_ratio, total_minions_killed, minions_killed_min,
                               vision_score, role, lane, summoner1Id, summoner2Id,
                               longest_time_spent_living, win, largest_multi_kill, penta_kills,
                               total_damage_dealt, gold_earned, first_Blood_Kill, items_in_match]
                
                
                runes_info = player['perks']['styles']
                
                # Nie zmienia id runy na nazwę ścieżki ;c
                # main_path = runes_info[0]['style']  # Główna ścieżka
                # sub_path = runes_info[1]['style']  # Dodatkowa ścieżka

                # aaa = Rune(region=region_from_dict, id=main_path)
                # bbb = aaa.path.name
 
                
                rune_names = []
                for rune_category in runes_info:
                    for rune_selection in rune_category['selections']:
                        rune = Rune(region=region_from_dict, id=rune_selection['perk'])  # Dodaj region do konstruktora Rune
                        # rune_path = Rune(region=region_from_dict, id = rune_selection['perk'])
                        # rune_path = rune_path.path.name
                        # ic(rune_path)
                        rune_names.append(rune.name)

                # Dodaj listę nazw run do informacji gracza
                player_info.append(rune_names)
                all_players_info.append(player_info)
                
                # ic(players_in_match)
                # ic(all_players_info)                              
                
            return all_players_info  # Zwracamy listę z informacjami o wszystkich graczach
            
        
        else:
            print("Error in the API request")
    except Exception as e:
        print("Error occurred:", e)  


def loop_through_matches(match_id, global_region):
        api_key = get_api_key()
        global_region2 = global_region_dictionary(global_region)
        api_url_match_info = f'https://{global_region2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        api_url = api_url_match_info + '?api_key=' + api_key

        resp = requests.get(api_url)
        data = resp.json()
        return data
        
def player_to_loop(puuid, match_data):

        wins = 0
        fb_kill = 0
        fb_assist = 0
        fb_participation = 0
        
        if 'metadata' in match_data and 'participants' in match_data['metadata']:
            part_index = match_data['metadata']['participants'].index(puuid)
        
        # part_index = match_data['metadata']['participants'].index(puuid)
            win = match_data['info']['participants'][part_index]['win']
            if win == True:
                wins = 1
            kills = match_data['info']['participants'][part_index]['kills']
            deaths = match_data['info']['participants'][part_index]['deaths']
            assists = match_data['info']['participants'][part_index]['assists']
            queue_id = match_data['info']['queueId']
            queue_name = queue_dictionary(queue_id)
            champion_name = match_data['info']['participants'][part_index]['championName']
            first_Blood_Kill = match_data['info']['participants'][part_index]['firstBloodKill']
            if first_Blood_Kill == True:
                fb_kill = 1
            
            first_blood_assist = match_data['info']['participants'][part_index]['firstBloodAssist']
            if first_blood_assist == True:
                fb_assist = 1
            
            if fb_kill == 1 or fb_assist == 1:
                fb_participation = 1
            
            if deaths == 0:
                kda = (kills + assists)
            else:
                kda = round((kills + assists) / deaths, 2)
            
            list = [wins, kda, champion_name, fb_participation]
            
            
        else:
            print('Metadata not found')
        
        return list

def process_looped_info(looped_info):
    total_wins = sum(item[0] for item in looped_info)
    
    # Obliczenie średniej KDA
    average_kda = mean([item[1] for item in looped_info])
    average_kda = round(average_kda, 2)
    # Znalezienie najczęściej występującego bohatera
    champions = [item[2] for item in looped_info]
    most_frequent_champion = Counter(champions).most_common(3)#[0][0]

    # Sumowanie pierwszych zabójstw
    fb_participations = (sum(item[3] for item in looped_info))

    return total_wins, average_kda, most_frequent_champion, fb_participations
    
# a = last_20_games_stats('PGiSiriQ2XpzwitWlp9EuOXk2KVNnO9C8wl5zczBKEkCJSBQic0vQ8vRIYCHf2vmLZtOj-u4COXnww')
# ic(a)


# a = get_general_match_info_by_id('EUN1_3528127260')
# # ic(a)
# matches = [
#     'EUN1_3528211755',
#     'EUN1_3528182528',
#     'EUN1_3528146098',
#     'EUN1_3528095469',
#     'EUN1_3526786395',
#     'EUN1_3526747280',
#     'EUN1_3526701835',
#     'EUN1_3526677399',
#     'EUN1_3526495714',
#     'EUN1_3526451919',
#     'EUN1_3526421680',
#     'EUN1_3513543232',
#     'EUN1_3513521847',
#     'EUN1_3513513284',
#     'EUN1_3513478355',
#     'EUN1_3513423571',
#     'EUN1_3512353454',
#     'EUN1_3512328052',
#     'EUN1_3511855420',
#     'EUN1_3512364838'
#     ]
# for match_id in matches:
#     match_data = loop_through_matches(match_id, 'EUN1')
#     ic(player_to_loop('PGiSiriQ2XpzwitWlp9EuOXk2KVNnO9C8wl5zczBKEkCJSBQic0vQ8vRIYCHf2vmLZtOj-u4COXnww', match_data))



# general_info = get_general_match_info_by_id('EUN1_3526786395') #flex?
# general_info = get_general_match_info_by_id('EUN1_3507241045') #normal
# general_info = get_general_match_info_by_id('EUN1_3507003256') #quickplay

# general_info = get_general_match_info_by_id('EUN1_3521502869') #aram

# ic(general_info)

