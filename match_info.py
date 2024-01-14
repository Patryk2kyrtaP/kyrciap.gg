import datetime
import requests
from icecream import ic

from config import get_api_key, setup_cassiopeia
from item_dictionary import item_dictionary
from player_profile_info import get_game_name_by_puuid
from region_dictionary import region_dictionary
from summoner_spell_dictionary import summoner_spells_dictionary
from cassiopeia import Rune
from region_dictionary import region_dictionary
from queue_dictionary import queue_dictionary


def get_match_id(puuid):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    api_url_match_v5_by_puuid = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20'
    api_url = api_url_match_v5_by_puuid + '&api_key=' + api_key

    try:
        resp = requests.get(api_url)
        print("Status Code:", resp.status_code)
        if resp.status_code == 200:
            match_id = resp.json()
            #print(match_id)
            return match_id
        
        else:
            print("Error in the API request")
    except Exception as e:
        print("Error occurred:", e)

def get_general_match_info_by_id(match_id):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    api_url_match_info = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
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
 
def get_match_info_by_id(match_id):
    # api_key = "RGAPI-cfa506a0-6ec1-4b84-9db0-d099dcf32566"
    api_key = get_api_key()
    api_url_match_info = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
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
                kda_ratio = round((kills + assists) / deaths, 2)  #Y
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
                summoner1Id = summoner_spells_dictionary(player['summoner1Id'])
                summoner2Id = summoner_spells_dictionary(player['summoner2Id'])
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


def last_20_games_stats(puuid):
    api_key = get_api_key()  # Replace with your API key
    api_url_matchlist = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    api_url = api_url_matchlist + '?api_key=' + api_key

    puuid = puuid
    
    our_summoner_name = get_game_name_by_puuid(puuid)
    
    try:
        resp = requests.get(api_url)
        if resp.status_code == 200:
            match_ids = resp.json()[:30]  
            # ic(match_ids)
            win_count = 0
            for match_id in match_ids:
                api_url_match_info = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
                api_url = api_url_match_info + '?api_key=' + api_key
                
                try:
                    resp = requests.get(api_url)
                    print("Status Code:", resp.status_code)
                    if resp.status_code == 200:
                        match_info = resp.json()
                        players_in_match = match_info['info']['participants'][:10]
                        
                        for player in players_in_match[:10]:
                            summoner_name = player['summonerName']
                            if summoner_name == our_summoner_name:
                                win = player['win']
                                # ic(win)
                                if win == True:
                                    win_count = win_count + 1
                                    
                  
                except Exception as e:
                    print("Error occurred:", e)  
                
            wins_in_20 = win_count
            win_percent = round((wins_in_20 / 20) * 100, 2)
                
            info_list = [wins_in_20, win_percent]
            return info_list 
 
        else:
            print("Error in the API request")
    except Exception as e:
        print("Error occurred:", e)

# a = last_20_games_stats('PGiSiriQ2XpzwitWlp9EuOXk2KVNnO9C8wl5zczBKEkCJSBQic0vQ8vRIYCHf2vmLZtOj-u4COXnww')
# ic(a)


# a = get_general_match_info_by_id('EUN1_3528127260')
# ic(a)




# general_info = get_general_match_info_by_id('EUN1_3526786395') #flex?
# general_info = get_general_match_info_by_id('EUN1_3507241045') #normal
# general_info = get_general_match_info_by_id('EUN1_3507003256') #quickplay

# general_info = get_general_match_info_by_id('EUN1_3521502869') #aram

# ic(general_info)

