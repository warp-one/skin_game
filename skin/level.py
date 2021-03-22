import libtcodpy as libtcod

import cellmap, settings, controls, environment

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

    w, h = settings.LVL0_MAP_WIDTH, settings.LVL0_MAP_HEIGHT

    def __init__(self, game):
        self.game = game

        self.time_since_update = 0.
        self.turn_clock = 0
        self.turn_actions = set()

        self.consoles = None
        self.create_consoles()
        self.camera = Camera(self)
        
        self.cellmap = cellmap.CellMap(self.w, self.h, self.consoles)
        #for c in self.cellmap.cells:
        #    self.turn_actions.add(  )
        self.player_controls = controls.KeyboardControls(self.cellmap)
        self.environment = environment.BasicEnvironment(self.cellmap, environment.test_rules)


    def create_consoles(self):
        self.background = libtcod.console_new(self.w, self.h)
        libtcod.console_set_default_background(self.background, libtcod.blue)
        self.fluids_layer = libtcod.console_new(self.w, self.h)
        libtcod.console_set_key_color(self.fluids_layer, libtcod.black)
        libtcod.console_set_default_background(self.fluids_layer, libtcod.blue)
        self.events_layer = libtcod.console_new(self.w, self.h)
        libtcod.console_set_key_color(self.fluids_layer, libtcod.black)
        libtcod.console_set_default_background(self.fluids_layer, libtcod.blue)
        self.hud_layer = libtcod.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        libtcod.console_set_default_background(self.hud_layer, libtcod.blue)
        self.consoles = {"background": self.background,
                         "fluids": self.fluids_layer,
                         "events": self.events_layer,
                         "hud": self.hud_layer}

    def update_all(self):
        self.time_since_update += libtcod.sys_get_last_frame_length()
        if self.time_since_update > 1.:
            self.time_since_update = 0.
            self.cellmap.update()
            self.turn_clock += 1
        if self.turn_clock >= 5:
            self.turn_clock = 0
            self.advance_turn()

    def render_all(self):
#        self.camera.move_camera(self.player.x, self.player.y)
        self.cellmap.draw()

    def clear_all(self):
#        for c in self.consoles:
#            libtcod.console_clear(c)
#        return
        libtcod.console_set_default_foreground(self.consoles["hud"], libtcod.black)  # selected_tile.color)
        for x in xrange(settings.SCREEN_WIDTH):
            for y in xrange(settings.SCREEN_HEIGHT):
                libtcod.console_put_char(self.consoles["hud"], x, y,
                                        ' ', libtcod.BKGND_NONE)
        if self.cellmap.cursor:
            x, y = self.cellmap.cursor.x, self.cellmap.cursor.y
            libtcod.console_put_char(self.hud_layer, x, y,
                                    ' ', libtcod.BKGND_NONE)
        libtcod.console_set_default_foreground(self.consoles["fluids"], libtcod.black)  # selected_tile.color)
        for x in xrange(50):
            for y in xrange(50):
                libtcod.console_put_char(self.consoles["fluids"], x, y,
                                        ' ', libtcod.BKGND_SET)

    def advance_turn(self):
        for action in self.turn_actions:
            action()
        self.environment.advance_environment_turn()
