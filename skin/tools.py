def xy_to_index(x, y, w):
    return y*w + x

def index_to_xy(i, w):
    return i%w, i/w
    
def adjacent_cell_index_pairs(w, h):
    size = w*h
    indexes = range(size)
    index_pairs = []
    for i in indexes:
        if (i+1)%w:
            index_pairs.append((i, i+1))
        if i/w < h - 1:
            index_pairs.append((i, i+w))
    return index_pairs
    
def mean(data):
    return sum(data)/float(len(data))