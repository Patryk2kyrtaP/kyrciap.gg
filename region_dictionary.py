def region_dictionary(region_id):
    region_dict = {
        'BR1': "BR",
        'EUN1': "EUNE",
        'EUW1': "EUW",
        'JP1': "JP",
        'KR': "KR",
        'LA1': "LAN",
        'LA2': "LAS",
        'NA1': "NA",
        'OC1': "OCE",
        'RU': "RU",
        'TR1': "TR",
    }
    
    region_name = region_dict.get(region_id, "Not a region")
    return region_name


# aaa = 'BR1'
# bbb = region_dictionary(aaa)
# print(bbb)