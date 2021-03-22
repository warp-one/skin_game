import libtcodpy as libtcod

import constants




class MapMode(object):
    def __init__(self,
                 tracked_stat,
                 low_color=libtcod.green,
                 high_color=libtcod.red,
                 num_color_indexes=10):
        self.stat = tracked_stat
        self.color_scale = [low_color, high_color]
        self.num_color_indexes = num_color_indexes
        self.color_indexes = [0, self.num_color_indexes]
        self.color_map = libtcod.color_gen_map(color_scale, color_indexes)


class IntegrityMapMode(MapMode):
    stat = "integrity"
    low_color = libtcod.red
    high_color = libtcod.lightest_sea
    color_scale = [low_color, high_color]
    num_color_indexes = 10
    color_indexes = [0, num_color_indexes]
    color_map = libtcod.color_gen_map(color_scale, color_indexes)


class TemperatureMapMode(MapMode):
    stat = "temperature"
    low_color = libtcod.darkest_red
    high_color = libtcod.yellow
    color_scale = [low_color, high_color]
    num_color_indexes = 10
    color_indexes = [0, num_color_indexes]
    color_map = libtcod.color_gen_map(color_scale, color_indexes)


class PerfusionMapMode(MapMode):
    stat = "perfusion"
    low_color = libtcod.darker_purple
    high_color = libtcod.fuchsia
    color_scale = [low_color, high_color]
    num_color_indexes = 10
    color_indexes = [0, num_color_indexes]
    color_map = libtcod.color_gen_map(color_scale, color_indexes)


class MoistureMapMode(MapMode):
    stat = "moisture"
    low_color = libtcod.lightest_crimson
    high_color = libtcod.azure
    color_scale = [low_color, high_color]
    num_color_indexes = 10
    color_indexes = [0, num_color_indexes]
    color_map = libtcod.color_gen_map(color_scale, color_indexes)


current_map_mode = None
available_map_modes = (IntegrityMapMode, MoistureMapMode, TemperatureMapMode, PerfusionMapMode)
