import libtcodpy as libtcod


def convert_text_to_Words(text):
    text_into_words = text.split()
    return [Word(w) for w in text_into_words]


class Word:
    def __init__(self, text):
        self._word = text
        self._current_letter = 0
        self.active = False
        self.active_color = libtcod.dark_gray
        self.active_letter_color = libtcod.red
        self.default_letter_color = libtcod.white

    def try_letter(self, letter, hard_try=True):
        word_response = "no effect"
        if not self.active:
            return "how did you get here?"
        if letter not in self._word:
            word_response = "miss"
        else:
            if self._word[self._current_letter] == letter:
                self.advance_current_letter()
                word_response = "complete"
            elif hard_try:
                self.reset_current_letter()
                word_response = "mistyped"
        return word_response

    def advance_current_letter(self):
        self._current_letter += 1
        if self._current_letter >= len(self._word):
            self.trigger_word()
            self.reset_current_letter()

    def trigger_word(self):
        print("You have typed %s!" % self._word)

    def reset_current_letter(self):
        self._current_letter = 0

    @property
    def letter_color_data(self):
        if self.active:
            letter_color = self.active_color
        else:
            letter_color = self.default_letter_color
        active_letter_colors = [self.active_letter_color]*self._current_letter
        num_unactivated_letters = len(self._word) - self._current_letter
        passive_letter_colors = [letter_color]*num_unactivated_letters
        letter_colors = active_letter_colors + passive_letter_colors
        return zip(self._word, letter_colors)

    @property
    def letters(self):
        return self._word
