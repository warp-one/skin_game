from fluids import *

def moisture(cell):
    wetness = [status.get_status("wet") for status in cell.statuses]
    return sum(filter(lambda x: x, wetness)) 

def create_status(name):
    if name == "blood":
        return Blood(1, 6)