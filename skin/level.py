from random import randint

import libtcodpy as libtcod

import printer, settings, word

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


class WordTypingManager:
    def __init__(self):
        self.words = set()

    def handle_letter(self, letter):
        for w in self.words:
            typing_attempt = w.try_letter(letter)
            if typing_attempt == "complete":
                pass
            elif typing_attempt == "miss":
                pass
            elif typing_attempt == "mistyped":
                pass
            else:
                raise NotImplementedError

    def add_word(self, word):
        word.active = True
        self.words.add(word)

    def remove_word(self, word):
        word.active = False
        self.words.remove(word)


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
        self.printers = set()
        self.word_manager = WordTypingManager()
        self.test_printer = printer.Printer(5, 5, 15, self.background)
        self.printers.add(self.test_printer)
        test_words = word.convert_text_to_Words("We are back in the caves. Is what the poster said in one corner.")
        for _ in range(4):
            self.word_manager.add_word(test_words[randint(0, len(test_words))])

        self.test_printer.add_text_to_words(test_words)
        self.player_controls = self.handle_keys

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
#            self.cellmap.update()
            self.turn_clock += 1
            self.tick_update()
        if self.turn_clock >= 5:
            self.turn_clock = 0
            self.advance_turn()

    def render_all(self):
#        self.camera.move_camera(self.player.x, self.player.y)
        for p in self.printers:
            p.draw()

    def clear_all(self):
        #for c in self.consoles:
        #    libtcod.console_clear(c)
        #return
        libtcod.console_set_default_foreground(self.consoles["hud"], libtcod.black)  # selected_tile.color)
        for x in xrange(settings.SCREEN_WIDTH):
            for y in xrange(settings.SCREEN_HEIGHT):
                libtcod.console_put_char(self.consoles["hud"], x, y,
                                        ' ', libtcod.BKGND_NONE)
        libtcod.console_set_default_foreground(self.consoles["fluids"], libtcod.black)  # selected_tile.color)
        for x in xrange(50):
            for y in xrange(50):
                libtcod.console_put_char(self.consoles["fluids"], x, y,
                                        ' ', libtcod.BKGND_SET)

    def advance_turn(self):
        for action in self.turn_actions:
            action()

    def tick_update(self):
        for p in self.printers:
            p.update()

    def handle_keys(self):
        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_ESCAPE:
            return True

        char = chr(key.c)
        if char in 'abcdefghijklmnopqrstuvwxyz':
            self.handle_letter(char)

    def handle_letter(self, l):
        print(l)
        self.word_manager.handle_letter(l)