def get_api_key():
    return "RGAPI-afefa65a-7532-43b7-88da-2c82568434b0"


import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


