import libtcodpy as libtcod

from skin import level, settings


class Game(object):
    def __init__(self, ww, wh):
        self.width, self.height = ww, wh
        
        libtcod.console_set_custom_font(settings.FONT_IMG,
                libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW,
                )
        libtcod.console_init_root(self.width, self.height, 
                'back into the caves', False, renderer=libtcod.RENDERER_SDL)
        libtcod.sys_set_fps(settings.LIMIT_FPS)

        self.current_level = level.Level(self)
        
        
    def execute(self):
        while not libtcod.console_is_window_closed():
#           libtcod.console_set_default_foreground(0, libtcod.white)
            self.current_level.update_all()
            self.current_level.render_all()
            libtcod.console_blit(self.current_level.background, 0, 0, 
                                 self.width, self.height, 0, 0, 0)
            libtcod.console_blit(self.current_level.hud_layer, 0, 0,
                                 self.width, self.height, 0, 0, 0,
                                 1.0,
                                 0.0)
            libtcod.console_flush()
            self.current_level.clear_all()
            exit = self.current_level.player_controls()
            if exit:
                break
        
if __name__ == '__main__':
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    game.execute()