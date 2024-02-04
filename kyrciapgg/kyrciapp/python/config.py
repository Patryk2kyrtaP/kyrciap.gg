def get_api_key():
    return "RGAPI-539638ad-113c-471b-92c4-afe13de380d7"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


