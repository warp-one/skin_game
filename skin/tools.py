def distance(p):
    return p[0] ** 2 + p[1] ** 2


def xy_to_index(x, y, w):
    return y * w + x


def index_to_xy(i, w):
    return i % w, i / w


def adjacent_cell_index_pairs(w, h):
    size = w * h
    indexes = range(size)
    index_pairs = []
    for i in indexes:
        if (i + 1) % w:
            index_pairs.append((i, i + 1))
        if i / w < h - 1:
            index_pairs.append((i, i + w))
    return index_pairs


def generate_N2(limit=None):
    ymax = [0]
    d = 0
    while limit is None or d <= limit:
        yieldable = []
        while True:
            batch = []
            for x in range(d + 1):
                y = ymax[x]
                if distance((x, y)) <= d ** 2:
                    batch.append((x, y))
                    ymax[x] += 1
            if not batch:
                break
            yieldable += batch
        yieldable.sort(key=distance)
        for p in yieldable:
            yield p
        d += 1
        ymax.append(0)


def generate_Z2(limit=None, origin=(0, 0)):
    def origin_correction(final_p):
        return final_p[0] + origin[0], final_p[1] + origin[1]

    for p in generate_N2(limit):
        yield origin_correction(p)
        if p[0] != 0:
            yield origin_correction((-p[0], p[1]))
        if p[1] != 0:
            yield origin_correction((p[0], -p[1]))
        if p[0] and p[1]:
            yield origin_correction((-p[0], -p[1]))


def mean(data):
    return sum(data) / float(len(data))


def xy_to_NSEW(x, y):
    return ((0, -1), (0, 1), (1, 0), (-1, 0))


CIRCLE_RANGE_1 = generate_Z2(limit=1)
CIRCLE_RANGE_2 = generate_Z2(limit=2)
