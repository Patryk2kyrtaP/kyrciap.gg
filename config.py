def get_api_key():
    return "RGAPI-13e84fa5-b0fd-4aaf-8a0c-e3f7b69b597c"


import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


