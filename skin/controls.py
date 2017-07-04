from random import choice

import libtcodpy as libtcod

class Cursor(object):
    def __init__(self, map_width, map_height, x=0, y=0):
        self.maxX, self.maxY = map_width - 1, map_height - 1
        self.x, self.y = x, y
        self.char = choice([libtcod.CHAR_CROSS, libtcod.CHAR_CHECKBOX_UNSET])
        
    def cursor_move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x >= self.maxX:
            self.x = self.maxX
        elif self.x < 0:
            self.x = 0
        if self.y >= self.maxY:
            self.y = self.maxY
        elif self.y < 0:
            self.y = 0
            
    def on_notify(self, entity, event):
        if event == "cursor move":
            self.cursor_move(*entity)
        
        


class KeyboardControls(object):
    def __init__(self, cellmap):
        self.cellmap = cellmap
        self.controlled_objects = []
        self.cellmap.cursor = Cursor(cellmap.w, cellmap.h)
        self.controls_add(self.cellmap.cursor)

    def handle_keys(self):
        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_ESCAPE:
            return True
            
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            direction = (0, -1)
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            direction = (0, 1)
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            direction = (-1, 0)
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            direction = (1, 0)
        else:
            direction = (0, 0)
        self.notify(direction, "cursor move")
            
    def controls_add(self, listener):
        self.controlled_objects.append(listener)
        
    def controls_remove(self, listener):
        self.controlled_objects.remove(listener)
        
    def notify(self, entity, event):
        for c in self.controlled_objects:
            c.on_notify(entity, event)
