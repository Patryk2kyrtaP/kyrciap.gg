
import requests
from config import get_api_key
from player_profile_info import get_summoner_info

def get_champion_stats(champion_name, server):
    api_key = get_api_key
    base_url = f'https://{server}.api.riotgames.com/lol'
    
    # Pobieranie listy championów
    response = requests.get(f'{base_url}/platform/v3/champions', params={'api_key': api_key})
    champions = response.json()['champions']
    
    # Znalezienie ID championa o nazwie champion_name
    champion_id = None
    for champ in champions:
        if champ['name'] == champion_name:
            champion_id = champ['id']
            break
    
    if champion_id is None:
        return f"Champion o nazwie {champion_name} nie istnieje na serwerze {server}"

    # Pobieranie statystyk championa
    response = requests.get(f'{base_url}/stats/v1/champion/{champion_id}', params={'api_key': api_key})
    champion_stats = response.json()
    
    # Wyświetlenie procentowego win ratio
    win_ratio = champion_stats['winRatio']
    return f"Procent wygranych meczów dla {champion_name} na serwerze {server}: {win_ratio}"

# Przykładowe użycie funkcji
champion_name = "Ahri"
server = "EUNE"
result = get_champion_stats(champion_name, server)
print(result)



def check_last_game_result(summoner_name, champion_name, api_key):
    # Krok 1: Pobierz puuid dla summoner_name
    summoner_info = get_summoner_info(summoner_name, api_key)
    puuid = summoner_info['puuid']

    # Krok 2: Pobierz listę ostatnich meczów
    last_match_id = get_last_match_id(puuid, api_key)

    # Krok 3: Sprawdź wynik ostatniej gry
    match_details = get_match_details(last_match_id, api_key)

    # Sprawdź, czy wybrana postać była w drużynie zwycięskiej
    for participant in match_details['info']['participants']:
        if participant['championName'] == champion_name and participant['win']:
            return True
    
    return False
