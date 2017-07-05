from random import choice

import libtcodpy as libtcod

import colors, constants, tools, controls, status


class SkinCell(object):
    
    
    def __init__(self, cellmap, color):
        self.cellmap = cellmap
        self._color = color
        self.char = ' '
        self.statuses = []
        
        self.temperature = constants.TEMP_SKIN_SURFACE_AVG
        self.moisture = constants.MOISTURE_SKIN_STARTING
        
    @property
    def color(self):
        return self._color
        
    @property
    def moisture(self):
        return self._moisture
        
    @moisture.setter
    def moisture(self, amt):
        if amt > 1.:
            amt = 1
        elif amt < 0.:
            amt = 0
        self._moisture = amt
        
    def dry(self):
        self.moisture += (self.status_percentage("wet") - self.moisture)
        
    def status_amount(self, adj):
        return sum([s.quality_amount(adj) for s in self.statuses])
        
    def status_percentage(self, adj):
        return reduce(tools.mean, [s.quality_percentage(adj) for s in self.statuses]) 
        
    def add_status(self, status_type):
        if status_type == "blood":
            for s in self.statuses:
                if s.name == "blood":
                    s.amount += 1
                break
            else:
                self.statuses.append(status.create_status("blood"))
        
        
    def update(self):
        #self.dry(heatmap, exposedmap)
        #self.break_out()
        #self.heal()
        #etc
        
        for s in self.statuses:
            if s.amount < 0.:
                self.statuses.remove(s)
            
            
class CellMap(object):
    def __init__(self, w, h, cons):
        self.w, self.h = w, h
        self.cell_con = cons["background"]
        self.fluids_con = cons["fluids"]
        self.hud_con = cons["hud"]
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
        
    def cell_get(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        return self.cells[i]
        
    def draw(self):
        for i, c in enumerate(self.cells):
            x, y = tools.index_to_xy(i, self.w)
            color = c.color
            char = c.char
#            x, y = self.game.camera.to_camera_coordinates(c.x, c.y)
            libtcod.console_set_char_background(self.cell_con, x, y, color)
            libtcod.console_set_default_foreground(self.cell_con, libtcod.dark_sepia)
            libtcod.console_put_char(self.cell_con, x, y, 
                                            char, libtcod.BKGND_NONE)
            if c.statuses:
                for s in c.statuses:
                    color = s.color
                    char = s.char
#                    libtcod.console_set_char_background(self.fluids_con, x, y, color)
                    libtcod.console_set_default_foreground(self.fluids_con, color)
                    libtcod.console_put_char(self.fluids_con, x, y, 
                                                    char, libtcod.BKGND_NONE)
                    
                                            
        if self.cursor:
            x, y, char = self.cursor.x, self.cursor.y, self.cursor.char
            libtcod.console_set_default_foreground(self.hud_con, libtcod.dark_sepia)
            libtcod.console_put_char(self.hud_con, x, y, 
                                            char, libtcod.BKGND_NONE)
            
                                            
    def update(self):
        for c in filter(lambda x: x, self.cells):
            c.update()
            
                                            
