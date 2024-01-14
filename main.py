import requests
import datetime
from icecream import ic

from config import get_api_key
from item_dictionary import item_dictionary
from player_profile_info import get_maestry_points, get_rank_info, get_summoner_info
from champion_dictionary import champ_dictionary
from match_info import get_match_id, get_match_info_by_id, last_20_games_stats
from match_info import get_general_match_info_by_id #, get_match_info_by_id
from region_dictionary import region_dictionary





#  wywołanie get_summoner_info -
#  informacje o graczu iconID/DataZmiany/Nick/Lvl/puuid/SummonerID

global_region = str(input("Enter account region: "))
# (AMERICAS/ EUROPE/ ASIA/ ESPORTS/ SEA/ )
summoner_name = str(input("Enter player's name: "))
summoner_info = get_summoner_info(summoner_name)

chosen_summoner_info = []
region = []
region_from_dict = str
encrypted_summoner_id = str


if summoner_info:
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

player_maestry_points = get_maestry_points(puuid)
ic(player_maestry_points)

player_rank_info = get_rank_info(encrypted_summoner_id)
ic(player_rank_info)

# last_20_games_info = last_20_games_stats(puuid)
# ic(last_20_games_info)

# otrzymujemy listę ostatnich 20 gier
match_id = get_match_id(puuid)
# print(match_id)

print("Available match IDs:")
for i, id in enumerate(match_id):
    print(f"{i + 1}. {id}")

try:
    selected_id = int(input("Select a match by entering its index: ")) - 1
    if 0 <= selected_id < len(match_id):
        selected_match_id = match_id[selected_id]
        # wywołanie get_match_info_by_id, informacje o meczu -
        # nazwy graczy/ kda/ przedmioty itd.
        general_match_info = get_general_match_info_by_id(selected_match_id)
        region = [general_match_info[4]]  
        
        # print(region_from_dict)
        # (region_dictionary(region_from_dict))
        
    else:
        print("Invalid index.")
except ValueError:
    print("Invalid input. Please enter a valid index.")




ic(general_match_info)
    
match_stats = get_match_info_by_id(selected_match_id)
print(match_stats)
