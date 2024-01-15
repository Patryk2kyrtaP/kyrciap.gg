import requests
import datetime
from icecream import ic
from collections import Counter
import numpy as np

from config import get_api_key
from item_dictionary import item_dictionary
from player_profile_info import get_maestry_points, get_rank_info, get_summoner_info
from champion_dictionary import champ_dictionary
from match_info import get_match_id, get_match_info_by_id, loop_through_matches, player_to_loop, process_looped_info
from match_info import get_general_match_info_by_id #, get_match_info_by_id
from region_dictionary import choose_region, region_dictionary, region_lists





#  wywołanie get_summoner_info -
#  informacje o graczu iconID/DataZmiany/Nick/Lvl/puuid/SummonerID


print("Enter account region: ")
global_region = choose_region()
ic(global_region)


summoner_name = str(input("Enter player's name: "))
summoner_info = get_summoner_info(summoner_name, global_region)

chosen_summoner_info = []
region = []
region_from_dict = str
encrypted_summoner_id = str
count = 20

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

player_maestry_points = get_maestry_points(puuid, global_region)
ic(player_maestry_points)

player_rank_info = get_rank_info(encrypted_summoner_id, global_region)
ic(player_rank_info)


# otrzymujemy listę gier
count = str(input('Enter matches count: (max 100)| '))
match_id = get_match_id(puuid, global_region, count)
# print(match_id)
matches = []

print("Available match IDs:")
for i, id in enumerate(match_id):
    matches.append(id)
    print(f"{i + 1}. {id}")

# ic(matches)

try:
    selected_id = int(input("Select a match by entering its index: ")) - 1
    if 0 <= selected_id < len(match_id):
        selected_match_id = match_id[selected_id]
        # wywołanie get_match_info_by_id, informacje o meczu -
        # nazwy graczy/ kda/ przedmioty itd.
        general_match_info = get_general_match_info_by_id(selected_match_id, global_region)
        region = [general_match_info[4]]  
        
        # print(region_from_dict)
        # (region_dictionary(region_from_dict))
        
    else:
        print("Invalid index.")
except ValueError:
    print("Invalid input. Please enter a valid index.")




ic(general_match_info)
    
match_stats = get_match_info_by_id(selected_match_id, global_region)
print(match_stats)


# ic(matches)
looped_info = []

for match_id in matches:
    match_data = loop_through_matches(match_id, global_region)
    # ic(match_data)
    looped_info.append(player_to_loop(puuid, match_data))

ic(looped_info)
processed_looped_info = process_looped_info(looped_info)
ic(processed_looped_info)
