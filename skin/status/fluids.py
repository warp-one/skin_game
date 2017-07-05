import libtcodpy as libtcod

class Status(object):
    is_ = []
    name = None
    
    def __init__(self, amount, max):
        self._amount = amount
        self.max_amount = max
        
    def quality_amount(self, quality):
        if quality in self.is_:
            return self.amount
        else:
            return 0
            
    def quality_percentage(self, quality):
        if quality in self.is_:
            return float(self.amount)/self.max_amount
        else:
            return 1.
            
    @property
    def amount(self):
        return self._amount
        
    @amount.setter
    def amount(self, amt):
        if amt > self.max_amount:
            amt = self.max_amount
        elif amt < 0.:
            amt = 0.
        self._amount = amt
            
            
class Blood(Status):
    is_ = ["wet", "food"]
    color = libtcod.red
    name = "blood"
    adjective = "bloody"
    
    @property
    def char(self):
        if self.amount > self.max_amount * 2/3:
            return libtcod.CHAR_BLOCK3
        elif self.amount > self.max_amount * 1/3:
            return libtcod.CHAR_BLOCK2
        else:
            return libtcod.CHAR_BLOCK1
    
class Sweat(Status):
    is_ = ["wet", "food"]
    color = libtcod.lighter_blue
    char = libtcod.CHAR_BLOCK2
    name = "sweat"
    adjective = "sweaty"