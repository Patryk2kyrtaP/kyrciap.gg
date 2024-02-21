def get_api_key():
    return "RGAPI-6338d1a1-8edd-44c5-94b7-0b9343b6c472"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


