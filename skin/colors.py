import libtcodpy as libtcod

LIGHT_SKIN_TONES = [libtcod.lightest_amber, 
                    libtcod.lightest_pink, 
                    libtcod.lightest_crimson,
                    libtcod.lightest_sepia,
                    ]
                    
SEBUM = libtcod.Color(227, 217, 145)
                    
FLORA_MALASSEZIA_COLOR = libtcod.Color(176, 69, 121)
FLORA_MALASSEZIA_MAP_COLOR = libtcod.light_green #libtcod.Color(206, 228, 209)
FLORA_STAPH_COLOR = libtcod.Color(215, 95, 0)
FLORA_STAPH_MAP_COLOR = libtcod.lighter_violet

EVENT_WOUND_BLOOD_PINK = libtcod.Color(255, 126, 126)
EVENT_WOUND_BLOOD_RED = libtcod.Color(203, 0, 0)
EVENT_WOUND_BLOOD_DEEP_RED = libtcod.Color(150, 11, 11)
EVENT_WOUND_BLOOD_DARK_RED = libtcod.Color(100, 11, 11)
EVENT_WOUND_BLOOD_DARK_PURPLE = libtcod.Color(57, 22, 52)
EVENT_WOUND_BLOOD_BLACK = libtcod.Color(31, 0, 0)
EVENT_WOUND_PUS_GREEN = libtcod.Color(202, 218, 0)
EVENT_WOUND_PUS_YELLOW = libtcod.Color(255, 248, 159)
EVENT_WOUND_PUS_DARK_YELLOW = libtcod.Color(162, 150, 0)
wound_colors = [EVENT_WOUND_BLOOD_PINK,
                EVENT_WOUND_BLOOD_RED,
                EVENT_WOUND_BLOOD_DEEP_RED,
                EVENT_WOUND_BLOOD_DARK_RED,
                EVENT_WOUND_BLOOD_DARK_PURPLE,
                EVENT_WOUND_BLOOD_BLACK]

MAP_INTEGRITY_HIGH = libtcod.green
MAP_INTEGRITY_LOW = libtcod.red
