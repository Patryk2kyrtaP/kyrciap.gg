def get_api_key():
    return "RGAPI-87da4184-4b63-421f-9767-fd6f011a048b"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


