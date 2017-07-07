from random import randint

import libtcodpy as libtcod

import tools



# Patterns
adjacent_NSEW = tools.adjacent_cell_index_pairs

# Dances
# i e, does blood flow
# does hair keep the skin warm
# does sweat cool it
# def temperature_sweat
def color_contest(A, B, _, _1):
    if not randint(0, 10):
        A._color, B._color = B._color, A._color
        
def migrate_disease(A, B):
    if not randint(0, 10):
        if (A.flora is None or B.flora is None) and A.flora != B.flora:
            source = (A if A.flora else B)
            destination = (B if source is A else A)
            if destination.habitability(source.flora) > source.habitability(source.flora): 
                destination.flora = source.flora
                source.flora = None
            
        
        
# Rules
# rule sets
test_rules = [migrate_disease]#[color_contest,]

# definitions
             



# Structures
class BasicEnvironment(object):
    def __init__(self, cellmap, rules):
        self.cellmap = cellmap
        self.cell_pairs = []
        self.cell_pair_interactions = rules
        self.create_cell_connections()
        
    def create_cell_connections(self, connection_pattern=adjacent_NSEW):
        w, h = self.cellmap.w, self.cellmap.h
        self.cell_pairs = connection_pattern(w, h)
        
    def run_cell_interactions(self):
        for a, b in self.cell_pairs:
            A, B = self.cellmap.cells[a], self.cellmap.cells[b]
            for interact in self.cell_pair_interactions:
                interact(A, B)
                
    def update(self):
        self.run_cell_interactions()
        for c in self.cellmap.cells:
            c.tick()