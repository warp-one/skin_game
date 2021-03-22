import libtcodpy as libtcod

import disease, terrain, map_modes


class MapEditor(object):

    keys = ['b', 'f', 'h', 'x', 'g', 's', 'i', 'q', 'w', 'p', 'r', 'a', 'z']

    def __init__(self, cellmap):
        self.cellmap = cellmap
        self.wound_size = 1
        
    def do(self, x, y, key):
        if key == 'b':
            self.cellmap.cell_get(x, y).status_add("blood")
        elif key == 'i':
            if self.wound_size == 1:
                self.cellmap.cell_get(x, y).status_add("wound")
            if self.wound_size == 2:
                for c in self.cellmap.area_get_cross(x, y):
                    if c is None:
                        continue
                    c.status_add("wound")
        elif key == 'f':
            self.cellmap.cell_get(x, y).flora = disease.Malassezia()
        elif key == 'g':
            self.cellmap.cell_get(x, y).flora = disease.StaphAureus()
        elif key == 'h':
            self.cellmap.cell_get(x, y).terrain = terrain.HairFollicle()
        elif key == 's':
            self.cellmap.cell_get(x, y).terrain = terrain.SebaceousGland()
        elif key == 'p':
            print self.cellmap.cell_get(x, y).info_list()
        elif key == 'w':
            self.wound_size += 1
            if self.wound_size > 2:
                self.wound_size = 1
        elif key == 'x':
            self.cellmap.cell_get(x, y).terrain = None
            self.cellmap.cell_get(x, y).flora = None
            self.cellmap.cell_get(x, y).statuses.clear()
        elif key == 'q':
            map_modes.current_map_mode = None
        elif key == 'r':
            if map_modes.current_map_mode is None:
                map_modes.current_map_mode = map_modes.available_map_modes[0]
            else:
                current_mode_index =  map_modes.available_map_modes.index(map_modes.current_map_mode)
                map_modes.current_map_mode = map_modes.available_map_modes[current_mode_index - 1]
        elif key == 'z':
            print self.cellmap.cell_bg_color(x, y)
            print getattr(self.cellmap.cell_get(x, y), map_modes.current_map_mode.stat)
