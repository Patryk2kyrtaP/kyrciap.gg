def get_api_key():
    return "RGAPI-03d49e19-3db7-4f49-a1f5-75d020438f47"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


