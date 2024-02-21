def get_api_key():
    return "RGAPI-85014bec-a87c-4329-9292-4f44171bc9a4"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


