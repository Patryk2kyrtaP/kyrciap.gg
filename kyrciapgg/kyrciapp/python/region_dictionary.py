from icecream import ic

def region_lists():
    region_list = [
        'BR1',
        'EUN1',
        'EUW1',
        'JP1',
        'KR',
        'LA1',
        'LA2',
        'NA1',
        'OC1',
        'PH2',
        'RU',
        'SG2',
        'TH2',
        'TR1',
        'TW2',
        'VN2',
        ]
    # ic(region_list)
    return region_list
        
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
        'PH2': "PH",
        'RU': "RU",
        'SG2': "SG",
        'TH2': "TH",
        'TR1': "TR",
        'TW2': "TW",
        'VN2': "VN",
    }
    
    region_name = region_dict.get(region_id, "Not a region")
    return region_name

def global_region_dictionary(region_id):
    global_region_dict = {
        'BR1': 'AMERICAS',
        'EUN1': 'EUROPE',
        'EUW1': 'EUROPE',
        'JP1': 'ASIA',
        'KR': 'ASIA',
        'LA1': 'AMERICAS',
        'LA2': 'AMERICAS',
        'NA1': 'AMERICAS',
        'OC1': 'ASIA',
        'PH2': 'ASIA',
        'RU': 'EUROPE',
        'SG2': 'ASIA',
        'TH2': 'ASIA',
        'TR1': 'EUROPE',
        'TW2': 'ASIA',
        'VN2': 'ASIA',
    }
    
    region_name = global_region_dict.get(region_id, "Not a region")
    return region_name

def choose_region():
    print("Available regions:")
    regions = region_lists()
    region_dict = {
        'BR1': 'Brazil',
        'EUN1': 'EUNE (Europe Nordic & East)',
        'EUW1': 'Europe West',
        'JP1': 'Japan',
        'KR': 'Korea',
        'LA1': 'Latin America North',
        'LA2': 'Latin America South',
        'NA1': 'North America',
        'OC1': 'Oceania',
        'PH2': 'Philippines',
        'RU': 'Russia',
        'SG2': 'Singapore',
        'TH2': 'Thailand',
        'TR1': 'Turkey',
        'TW2': 'Taiwan',
        'VN2': 'Vietnam',
    }
    return list(region_dict.items())
    # for i, region in enumerate(regions):
    #     translated_region = region_dict.get(region, "Unknown Region")
    #     print(f"{i + 1}. {translated_region} ({region})")
    
    # while True:
    #     try:
    #         choice = int(input("Choose a region by entering its number: "))
    #         if 1 <= choice <= len(regions):
    #             selected_region = regions[choice - 1]
    #             return selected_region
    #         else:
    #             print("Invalid choice. Please enter a valid number.")
    #     except ValueError:
    #         print("Invalid input. Please enter a number.")

# selected_region = choose_region()
# print(f"Selected region: {selected_region}")