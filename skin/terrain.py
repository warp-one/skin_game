import libtcodpy as libtcod

class Terrain(object):
    char = '.'
    color = libtcod.black
    name = "an unremarkable blemish"
    
    
class HairFollicle(Terrain):
    char = 'l'
    color = libtcod.dark_sepia
    name = "hair"
    
class SebaceousGland(Terrain):
    char = '.'
    color = libtcod.white
    name = "gland"