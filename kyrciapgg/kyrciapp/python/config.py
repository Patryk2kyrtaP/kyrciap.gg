def get_api_key():
    return "RGAPI-196b9db9-4f70-40f3-bb3c-4d8a264d9eef"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


