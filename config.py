def get_api_key():
    return "RGAPI-f8d6adad-8196-44fd-ad6c-4c871b6337c2"

import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


