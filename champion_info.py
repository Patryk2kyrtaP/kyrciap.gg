
import requests
from config import get_api_key

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
