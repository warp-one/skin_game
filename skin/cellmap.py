from random import choice, randint

import libtcodpy as libtcod

import colors, constants, tools, controls, status


CALCULATED_MOISTURE_TENDENCY = .3


class SkinCell(object):
    
    
    def __init__(self, cellmap, color):
        self.cellmap = cellmap
        self._color = color
        self._char = ' '
        self.statuses = {}
        self.terrain = None
        self.flora = None
        self.location = None
        
        self.temperature = constants.TEMP_SKIN_SURFACE_AVG
        self.moisture = constants.MOISTURE_SKIN_STARTING
        
    @property
    def char(self):
        if self.terrain:
            return self.terrain.char
        else:
            return self._char
        
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
        return sum([s.quality_amount(adj) for s in self.statuses.values()])
        
    def status_percentage(self, adj):
        try:
            return reduce(tools.mean, [s.quality_percentage(adj) for s in self.statuses.values()])
        except TypeError:
            return 0.
        
    def status_add(self, status_type, amt=1):
        if status_type in self.statuses:
            self.statuses[status_type].amount += amt
        else:
            if amt > 0:
                self.statuses[status_type] = status.create_status(status_type, amt=amt)
                
    def status_get(self, status_type):
        try:
            return self.statuses[status_type]
        except KeyError:
            return False
            
    def habitability(self, germ):
        surpluses = []
        for r in germ.required_resources:
            required_amount = germ.required_resources[r]
            current_amount = self.status_amount(r)
            if current_amount < required_amount:
                return -1
            pct_surplus = (current_amount - required_amount)/float(required_amount)
            surpluses.append(pct_surplus)
        return sum(surpluses)/len(surpluses)
                
    def sweat(self):
        if self.terrain and self.terrain.name == "hair":
            will_sweat = not randint(0, 15)
        else:
            will_sweat = not randint(0, 220)
        if will_sweat:
            self.status_add("sweat")
        if self.terrain and self.terrain.name == "gland":
            if not randint(0, 5):
                excretion_field = self.cellmap.area_get_cross(*self.location)
                for tile in excretion_field:
                    if "sebum" in tile.statuses:
                        continue
                    tile.status_add("sebum")
                    break
            
            
    def sweat_evaporate(self):
        #if self.status_percentage("wet") > CALCULATED_MOISTURE_TENDENCY:
        if not randint(0, 4):
            self.status_add("sweat", amt=-1)
            
        
    def info_list(self):
        info = ["A patch of skin. It's about {0} degrees.".format(self.temperature)]
        for t in filter(lambda x: x, (self.terrain, self.flora)):
            info.append(t.name)
        for s in self.statuses:
            info.append((s + ' ' + str(self.statuses[s].amount)))
        return info
        
    def tick(self):
        self.sweat()
        self.sweat_evaporate()
                
    def update(self):
        #self.dry(heatmap, exposedmap)
        #self.break_out()
        #self.heal()
        #etc
        
        for s in self.statuses.values():
            if s.amount <= 0:
                del self.statuses[s.name]
                
            
class CellMap(object):

    hud_location = (30, 0)

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
        cell.location = (x, y)
        
    def cell_remove(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        self.cells[i] = None
        
    def cell_get(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        try:
            return self.cells[i]
        except IndexError:
            return None
        
    def area_get_cross(self, x, y):
        a = [self.cell_get(cx, cy) for (cx, cy) in tools.generate_Z2(limit=1, origin=(x, y))]
        #a = [self.cell_get(cx, cy) for (cx, cy) in [(x + p[0], y + p[1]) for p in tools.CIRCLE_RANGE_1]]
        return a
        
  #  def cell_find_status(self, ox, oy, status_type, 
        
#    def evaporate(self):
#        sweat_cells = filter(lambda x: x.status_get("sweat"), self.cells)
#        if len(sweat_cells)/len(self.cells)
        
    def draw(self):
        for i, c in enumerate(self.cells):
            x, y = tools.index_to_xy(i, self.w)
            bgcolor = c.color
            fgcolor = (c.terrain.color if c.terrain else libtcod.black)
            char = c.char
#            x, y = self.game.camera.to_camera_coordinates(c.x, c.y)
            libtcod.console_set_char_background(self.cell_con, x, y, bgcolor)
            libtcod.console_set_default_foreground(self.cell_con, fgcolor)
            libtcod.console_put_char(self.cell_con, x, y, 
                                            char, libtcod.BKGND_NONE)
            if c.statuses or c.flora:
                if c.statuses:
                    for s in c.statuses.values():
                        bgcolor = s.color
                        char = s.char
                
                if c.flora:
                    char = c.flora.char
                    fgcolor = c.flora.color
                    bgcolor = libtcod.color_lerp(bgcolor, c.flora.bgcolor, .5)
#                        libtcod.console_set_char_background(self.fluids_con, x, y, bgcolor)
                libtcod.console_set_char_background(self.fluids_con, x, y, bgcolor)
                libtcod.console_set_default_foreground(self.fluids_con, fgcolor)
                libtcod.console_put_char(self.fluids_con, x, y, 
                                                char, libtcod.BKGND_NONE)
            else:
                libtcod.console_set_char_background(self.fluids_con, x, y, libtcod.black)

                    
                                            
        if self.cursor:
            x, y, char = self.cursor.x, self.cursor.y, self.cursor.char
            libtcod.console_set_default_foreground(self.hud_con, libtcod.dark_sepia)
            libtcod.console_put_char(self.hud_con, x, y, 
                                            char, libtcod.BKGND_NONE)
                                            
            selected_tile = self.cell_get(self.cursor.x, self.cursor.y)
            if selected_tile:
                for j, item in enumerate(selected_tile.info_list()):
                    for i, c in enumerate(item):
                        x, y = self.hud_location[0] + i, self.hud_location[1] + j 
                        libtcod.console_set_default_foreground(self.hud_con, selected_tile.color)
                        libtcod.console_put_char(self.hud_con, x, y, 
                                                        c, libtcod.BKGND_NONE)
                    
            
                                            
    def update(self):
        for c in filter(lambda x: x, self.cells):
            c.update()
            
                                            
