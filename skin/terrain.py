import libtcodpy as libtcod

class Terrain(object):
    char = '.'
    color = libtcod.black
    
class HairFollicle(Terrain):
    char = 'l'
    color = libtcod.dark_sepia