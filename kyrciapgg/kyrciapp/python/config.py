def get_api_key():
    return "RGAPI-509d70ee-769e-488c-a741-adaa4e115141"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


