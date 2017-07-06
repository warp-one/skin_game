import colors

class Disease(object):
    name = "disease"
    water_min = 0.1
    water_max = 1.0
    def __init__(self):
        pass
        
class Malassezia(Disease):
    name = "Malassezia"
    flora_type = "fungus"
    char = 'p'
    color = colors.FLORA_MALASSEZIA_COLOR
    bgcolor = colors.FLORA_MALASSEZIA_MAP_COLOR