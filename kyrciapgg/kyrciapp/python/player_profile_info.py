import requests
import datetime
from datetime import datetime
from icecream import ic
from kyrciapp.python.champion_dictionary import champ_dictionary
from kyrciapp.python.config import get_api_key, setup_cassiopeia
import cassiopeia as cass

from kyrciapp.python.region_dictionary import global_region_dictionary

def get_summoner_info(summoner_name, global_region):
    api_key = get_api_key()
    # global_region2 = global_region_dictionary(global_region)
    api_url = f"https://{global_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    api_url = api_url + '?api_key=' + api_key
    
    # setup_cassiopeia()
    
    try:
        resp = requests.get(api_url)
        if resp.status_code == 200:
            player_info = resp.json()
            account_Id = player_info['accountId']
            profile_Icon_Id = player_info['profileIconId']
            revision_Date = player_info['revisionDate']
            name = player_info['name']
            id = player_info['id']
            puuid1 = player_info['puuid']
        #     summoner = cass.Summoner(account_id=id, region = 'EUN1')
        # # Uzyskaj region gracza
        #     region = summoner.region
        #     ic(region)
            summoner_Level = player_info['summonerLevel']

            player_info_list = [account_Id, 
                                profile_Icon_Id,    
                                revision_Date,      
                                name,               
                                id,                 
                                puuid1,              
                                summoner_Level]     
            # ic(player_info_list)
            return player_info_list
        
        
            
        else:
            print("Error in the API request")
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

# rank info
def get_rank_info(encrypted_summoner_id, global_region):
    api_key = get_api_key()
    api_url = f"https://{global_region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}?api_key={api_key}"

    try:
        resp = requests.get(api_url)
        if resp.status_code == 200:
            rank_infos = resp.json()
            if rank_infos:
                solo_q_info = None
                flex_info = None

                for info in rank_infos:
                    queue_type = info['queueType']
                    if queue_type == 'RANKED_SOLO_5x5':
                        solo_q_info = extract_rank_info(info)
                    elif queue_type == 'RANKED_FLEX_SR':
                        flex_info = extract_rank_info(info)

                # ic(solo_q_info)
                # ic(flex_info)
                
                return solo_q_info, flex_info
                
            else:
                print('No ranked games played.')
                return None, None  # Zwróć krotkę dwóch wartości None
        else:
            print("Error in the API request")
            return None, None
    except Exception as e:
        print("Error occurred:", e)
        ic(e)
        return None

def extract_rank_info(info):
    tier = info['tier']
    rank = info['rank']
    leaguePoints = info['leaguePoints']
    wins = info['wins']
    losses = info['losses']
    games_played = wins + losses
    win_percentage = int((wins / games_played) * 100) if games_played > 0 else 0
    veteran = info['veteran']
    inactive = info['inactive']
    freshBlood = info['freshBlood']
    hotStreak = info['hotStreak']
    
    rank_info = {
        "Tier": tier,
        "Rank": rank,
        "League_Points": leaguePoints,
        "Wins": wins,
        "Losses": losses,
        "Games_Played": games_played,
        "Win_Percentage": f'{win_percentage}%',
        "Veteran": veteran,
        "Inactive": inactive,
        "Fresh_Blood": freshBlood,
        "Hot_Streak": hotStreak
    }

    return rank_info

#champion maestry
def get_maestry_points(puuid, global_region):
    api_key = get_api_key()
    api_url = f"https://{global_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=10"
    api_url = api_url + '&api_key=' + api_key
    
    try:
        resp = requests.get(api_url)
        if resp.status_code == 200:
            maestry_info = resp.json()
            champions_maestry = []

            for champion in maestry_info:
                chestGranted = champion['chestGranted']
                champion_id = champion['championId']
                champion_name = champion_id  # Przekazanie identyfikatora mistrza jako liczby całkowitej
                last_play_time = champion['lastPlayTime']
                last_play_date = datetime.fromtimestamp(last_play_time / 1000.0).strftime('%d/%m/%Y')
                champion_level = champion['championLevel']
                champion_points = champion['championPoints']
                
                champion_maestry_info = [chestGranted,
                                      champion_name,
                                      last_play_date,
                                      champion_level,
                                      champion_points]

                champions_maestry.append(champion_maestry_info)
            
            return champions_maestry
            
            
        else:
            print("Error in the API request")
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None    


def get_game_name_by_puuid(puuid, global_region):
    api_key  = get_api_key()
    global_region2 = global_region_dictionary(global_region)
    api_url = f'https://{global_region2}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    api_url = api_url + '?api_key=' + api_key
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            account_info = response.json()
            game_name = account_info['gameName']
            # ic(game_name)
            return game_name
        else:
            print("Error in the API request:", response.status_code)
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

# game_name = get_game_name_by_puuid('PGiSiriQ2XpzwitWlp9EuOXk2KVNnO9C8wl5zczBKEkCJSBQic0vQ8vRIYCHf2vmLZtOj-u4COXnww')



# get_summoner_info('Patryk2kyrtaP')
# ic(a)# aa= get_maestry_points('1_5EXnxn4aylW6qxCaqEcYbqrCIn4VWnGzS96IDjmx2V_uJY3S-odoyT5Mi3HwwBUDmEpol6G0Jsrg')
# ic(aaa)


# b = get_rank_info('mZhbFG-CidjQZuQieKA1w5wmcwMMEJ0wHHf5ftHviHUvugg') #Stonred
# ic(b)

# zmienna1 = get_rank_info('3I92-tDHxiOSUKdakDlrY7TMDUk7XxjbXKXqCt5FkQwCk_c') #HudsonBos
# ic(zmienna1)
 
# get_rank_info('WyXgGXr6PcSG9OxTx1l3dTjCoNpBU1TiWMQhb3XEu2GjxrmCFxycuQUa4A')