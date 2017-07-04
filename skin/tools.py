def xy_to_index(x, y, w):
    return y*w + x

def index_to_xy(i, w):
    return i%w, i/w