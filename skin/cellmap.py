from random import choice

import libtcodpy as libtcod

import colors, constants, tools, controls

class SkinCell(object):
    
    
    def __init__(self, cellmap, color):
        self.cellmap = cellmap
        self._color = color
        self.char = ' '
        self.statuses = []
        
        self.temperature = constants.TEMP_SKIN_SURFACE_AVG
        
    @property
    def color(self):
        return self._color
        
    def update(self):
        pass
            
            
class CellMap(object):
    def __init__(self, w, h, con):
        self.w, self.h = w, h
        self.con = con
        self.cells = [None] * self.size
        self.cursor = None
        for x in range(w):
            for y in range(h):
                self.cell_add(x, y, SkinCell(self, choice(colors.LIGHT_SKIN_TONES)))
        
    @property
    def size(self):
        return self.w * self.h
        
    def cell_add(self, x, y, cell):
        i = tools.xy_to_index(x, y, self.w)
        self.cells[i] = cell
        
    def cell_remove(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        self.cells[i] = None
        
    def draw(self):
        for i, c in enumerate(self.cells):
            x, y = tools.index_to_xy(i, self.w)
            color = c.color
            char = c.char
#            x, y = self.game.camera.to_camera_coordinates(c.x, c.y)
            libtcod.console_set_char_background(self.con, x, y, color)
            libtcod.console_set_default_foreground(self.con, libtcod.dark_sepia)
            libtcod.console_put_char(self.con, x, y, 
                                            char, libtcod.BKGND_NONE)
                                            
        if self.cursor:
            x, y, char = self.cursor.x, self.cursor.y, self.cursor.char
            libtcod.console_set_default_foreground(self.con, libtcod.black)
            libtcod.console_put_char(self.con, x, y, 
                                            char, libtcod.BKGND_NONE)
            
                                            
    def update(self):
        for c in filter(lambda x: x, self.cells):
            c.update()
                                            
                                            
