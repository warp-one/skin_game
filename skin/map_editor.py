class MapEditor(object):

    keys = ['b']

    def __init__(self, cellmap):
        self.cellmap = cellmap
        
    def do(self, x, y, key):
        if key == 'b':
            self.cellmap.cell_get(x, y).add_status("blood")