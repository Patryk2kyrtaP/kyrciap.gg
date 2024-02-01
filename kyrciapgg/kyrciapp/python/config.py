def get_api_key():
    return "RGAPI-96b86f43-8833-4f7c-ad18-c68cbd19d643"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


