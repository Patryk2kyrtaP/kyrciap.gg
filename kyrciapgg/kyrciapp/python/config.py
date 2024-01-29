def get_api_key():
    return "RGAPI-698b36f2-a7a3-41a5-a01a-52b54a6872e3"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


