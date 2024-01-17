def get_api_key():
    return "RGAPI-119dab26-2399-42af-9404-2321d08a3dfc"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


