import disease, terrain

class MapEditor(object):

    keys = ['b', 'f', 'h', 'x', 'g']

    def __init__(self, cellmap):
        self.cellmap = cellmap
        
    def do(self, x, y, key):
        if key == 'b':
            self.cellmap.cell_get(x, y).status_add("blood")
        elif key == 'f':
            self.cellmap.cell_get(x, y).flora = disease.Malassezia()
        elif key == 'g':
            self.cellmap.cell_get(x, y).flora = disease.StaphAureus()
        elif key == 'h':
            self.cellmap.cell_get(x, y).terrain = terrain.HairFollicle()
        elif key == 'x':
            self.cellmap.cell_get(x, y).terrain = None
            self.cellmap.cell_get(x, y).flora = None
            self.cellmap.cell_get(x, y).statuses.clear()