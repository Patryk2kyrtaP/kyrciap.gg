def queue_dictionary(queue_id):
    queue_dict = {
        400: "Normal (Blind pick)",
        420: "Ranked Solo",
        430: "Normal (Draft)",
        440: "Ranked Flex",
        450: "ARAM",
        700: "Clash",
        830: "Ranked TFT",
        850: "Normal TFT",
        900: "ARURF",
        1020: "One for All",
        1200: "Nexus Blitz", 
        1700: "Game took place too long ago"
    }
    
    queue_name = queue_dict.get(queue_id, "Invalid")
    return queue_name


# aaa = '420'
# bbb = queue_dictionary(aaa)
# print(bbb)