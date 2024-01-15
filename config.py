def get_api_key():
    return "RGAPI-15e85bc4-b9fd-4a62-b8f5-562a8b7cd47d"


import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


