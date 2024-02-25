import os


def get_api_key():
    return "RGAPI-464a80b1-1861-41ff-a7b5-ead15641d6c7"
    #return os.getenv('RIOT_API_KEY')


import cassiopeia as cass
def setup_cassiopeia():
    api_key = get_api_key()
    cass.set_riot_api_key(api_key)


