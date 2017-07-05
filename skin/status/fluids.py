import libtcodpy as libtcod

class Status(object):
    is_ = []
    char = '?'
    colors = (libtcod.green)
    name = "a mysterious substance"
    adjective = "sticky"
    
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
            
    @property
    def color(self):
        return self.colors[int(float(self.amount)/self.max_amount*(len(self.colors) - 1))]
            
class Blood(Status):
    is_ = ["wet", "food"]
    name = "blood"
    adjective = "bloody"
    colors = (libtcod.lighter_red, libtcod.light_red,
              libtcod.red, libtcod.dark_red)
    
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
    colors = (libtcod.lighter_blue, libtcod.light_blue,
              libtcod.blue)
    name = "sweat"
    adjective = "sweaty"
    
    
class DriedBlood(Blood):
    is_ = ["food"]
    color = libtcod.darkest_red
    name = "dried blood"