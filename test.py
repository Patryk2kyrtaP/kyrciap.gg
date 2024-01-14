import requests
from config import get_api_key
from icecream import ic
api_key = get_api_key()

def get_previous_season_rank(summoner_id, api_key, previous_season):
    
    url = f"https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    ic(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ranks = response.json()
            # ic(ranks)
            # Filtrowanie danych z odpowiedniego sezonu
            previous_season_rank = [rank for rank in ranks if rank['season'] == previous_season]
            return previous_season_rank
        else:
            print("Error in the API request")
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

# Wywołanie funkcji z przykładowymi danymi


summoner_id = "8wGJR1PVWt8eAoozGsiYzKz-ZQve2O3pHyJXouRkL2K4k34" #vugen
previous_season = 'S12' # Przykładowy sezon
previous_season_rank_info = get_previous_season_rank(summoner_id, api_key, previous_season)
print(previous_season_rank_info)
