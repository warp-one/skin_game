import libtcodpy as libtcod

import cellmap, settings, controls

class Camera(object):
    
    camera_x = 0
    camera_y = 0
    
    def __init__(self, level):
        self.map_width, self.map_height = settings.LVL0_MAP_WIDTH, settings.LVL0_MAP_HEIGHT
        self.w = settings.SCREEN_WIDTH
        self.h = settings.SCREEN_HEIGHT

    def to_camera_coordinates(self, x, y):
        x, y = x - self.camera_x, y - self.camera_y
        return x, y
        
    def move_camera(self, target_x, target_y):
        x = target_x - self.w/2
        y = target_y - self.h/2
        
        if x < 0: x = 0
        if y < 0: y = 0
        x_overset = self.map_width - self.w - 1
        y_overset = self.map_height - self.h - 1
        if x > x_overset: x = x_overset
        if y > y_overset: y = y_overset
        
        self.camera_x, self.camera_y = x, y


class Level(object):

    w, h = 30, 30

    def __init__(self, game):
        self.game = game
        self.create_consoles()
        self.cellmap = cellmap.CellMap(self.w, self.h, self.background)
        self.camera = Camera(self)
        self.player_controls = controls.KeyboardControls(self.cellmap)
        
    def create_consoles(self):
        self.background = libtcod.console_new(self.w, self.h)
        self.foreground = libtcod.console_new(self.w, self.h)
        libtcod.console_set_default_background(self.background, libtcod.blue)

    def update_all(self):
        self.cellmap.update()
            
    def render_all(self):
#        self.camera.move_camera(self.player.x, self.player.y)
        self.cellmap.draw()

    def clear_all(self):
        for x in xrange(settings.SCREEN_WIDTH):
            for y in xrange(settings.SCREEN_HEIGHT):
                libtcod.console_put_char(self.foreground, x, y, 
                                ' ', libtcod.BKGND_NONE)
