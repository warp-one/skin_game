from .. import constants
from fluids import *
from wounds import Wound

def moisture(cell):
    wetness = [status.get_status("wet") for status in cell.statuses]
    return sum(filter(lambda x: x, wetness)) 

def create_status(name, amt=1):
    if name == "blood":
        return Blood(amt, constants.SKIN_MAX_BLOOD)
    elif name == "sweat":
        return Sweat(amt, constants.SKIN_MAX_SWEAT)
    elif name == "sebum":
        return Sebum(amt, constants.SKIN_MAX_WAX)
    elif name == "wound":
        return Wound(amt, constants.SKIN_WOUND_LEVELS)