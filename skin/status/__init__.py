from fluids import *

def moisture(cell):
    wetness = [status.get_status("wet") for status in cell.statuses]
    return sum(filter(lambda x: x, wetness)) 

def create_status(name, amt=1):
    if name == "blood":
        return Blood(amt, 4)
    elif name == "sweat":
        return Sweat(amt, 6)
    elif name == "sebum":
        return Sebum(amt, 3)