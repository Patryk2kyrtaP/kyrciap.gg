def summoner_spells_dictionary(summoner_id):
    summoner_spell_dict = {
        21: "Barrier",
        1: "Cleanse",
        2202: "Flash",
        2201: "Flee",
        14: "Ignite",
        3: "Exhaust",
        4: "Flash",
        6: "Ghost",
        7: "Heal",
        13: "Clarity",
        30: "To the King!",
        31: "Poro Toss",
        11: "Smite",
        39: "Mark",
        32: "Mark",
        12: "Teleport",
        54: "Placeholder",
        55: "Placeholder and Attack-Smite",
    }
    
    summoner_spell_name = summoner_spell_dict.get(summoner_id, "Empty slot")
    return summoner_spell_name
