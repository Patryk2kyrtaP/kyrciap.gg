def get_api_key():
    return "RGAPI-a16f4f27-2cae-44fb-b118-14db5f2f771d"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


