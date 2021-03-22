import random

from .. import colors
from fluids import Status


class Wound(Status):
    char = None
    color_options = colors.wound_colors
    bgcolor_options = colors.wound_colors
    name = "wound"
    adjective = "damaged"

    def __init__(self, *args, **kwargs):
        super(Wound, self).__init__(*args, **kwargs)
        self.distance_to_intact_skin = 0

    def get_color(self):
        return random.choice(self.color_options)

    def get_bgcolor(self):
        bgcolor_depth = len(self.bgcolor_options) - 1
        if self.count <= bgcolor_depth:
            color_index = self.count
        else:
            color_index = bgcolor_depth
        return self.bgcolor_options[color_index]
