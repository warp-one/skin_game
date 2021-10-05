import libtcodpy as libtcod

import word


class Printer:
    def __init__(self, x, y, width, console):
        self.words = []
        self.forme = [[]]
        self.x, self.y = x, y
        self.width = width
        self.console = console
        self.default_bgcolor = libtcod.black
        self.default_fgcolor = libtcod.white
        self.effects = []

    def add_text_to_words(self, words_to_add):
        self.words += words_to_add
        self.create_forme()

    def create_forme(self):
        self.forme = [[]]
        current_row_index = 0
        current_row_length = 0
        current_row = self.forme[current_row_index]
        for w in self.words:
            if current_row_length + len(w.letters) > self.width:
                current_row_index += 1
                self.forme.append([])
                current_row = self.forme[current_row_index]
                current_row_length = 0
            current_row.append(w)
            current_row_length += len(w.letters) + 1

    def draw(self):
        chars_drawn = 0
        for e in self.effects:
            e.reset()
        for current_row, row in enumerate(self.forme):
            current_col = 0
            for w in row:
                for letter, color in w.letter_color_data:
                    x = self.x + current_col
                    y = self.y + current_row
                    for e in self.effects:
                        letter, color = e.letterstream(letter, color)
                    libtcod.console_set_char_background(self.console, x, y, self.default_bgcolor)
                    libtcod.console_set_default_foreground(self.console, color)
                    libtcod.console_put_char(self.console, x, y,
                                             letter, libtcod.BKGND_NONE)
                    current_col += 1
                    chars_drawn += 1
                current_col += 1    # space between words
                chars_drawn += 1

    def update(self):
        for e in self.effects:
            e.update()