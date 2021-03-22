from random import choice, randint

import libtcodpy as libtcod

import colors, constants, tools, status, terrain, disease, map_modes

CALCULATED_MOISTURE_TENDENCY = .3


class SkinCell(object):

    def __init__(self, cellmap, color):
        self.cellmap = cellmap
        self._color = color
        self._char = ' '
        self.statuses = {}
        self.terrain = None
        self.flora = None
        self.location = None

    @property
    def temperature(self):
        w = constants.SKIN_WOUND_LEVELS/2 * 1.0
        return constants.TEMP_SKIN_SURFACE_AVG + (constants.WOUND_HEAT_SCALE * (w -abs(w - self.status_amount("wound"))))

    @property
    def temperature_scaled(self):
        return (self.temperature - constants.SKIN_MIN_TEMPERATURE)/(constants.SKIN_MAX_TEMPERATURE - constants.SKIN_MIN_TEMPERATURE)

    @property
    def moisture(self):
        return self.status_amount("wound") + self.status_amount("sweat") + self.status_amount("blood")

    @property
    def moisture_scaled(self):
        return self.moisture/constants.SKIN_MAX_MOISTURE

    @property
    def integrity(self):
        return 1.0 - (self.status_amount("wound")/constants.SKIN_WOUND_LEVELS)

    @property
    def perfusion(self):
        return 1.0

    @property
    def char(self):
        if self.terrain:
            return self.terrain.char
        else:
            return self._char

    @property
    def color(self):
        if self.status_amount("wound") > 2.0:
            return libtcod.darker_red
        else:
            return self._color

    def status_quality_amount(self, adj):
        return sum([s.quality_amount(adj) for s in self.statuses.values()])

    def status_percentage(self, adj):
        try:
            return reduce(tools.mean, [s.quality_percentage(adj) for s in self.statuses.values()])
        except TypeError:
            return 0.

    def status_add(self, status_type, amt=1):
        if status_type in self.statuses:
            self.statuses[status_type].amount += amt
        else:
            if amt > 0:
                self.statuses[status_type] = status.create_status(status_type, amt=amt)

    def status_get(self, status_type):
        try:
            return self.statuses[status_type]
        except KeyError:
            return None

    def status_amount(self, status_type):
        level = self.status_get(status_type)
        if level is None:
            return 0.0
        else:
            return level.amount * 1.0

    def nearby_status_count(self, status_name):
        distances_to_no_status = []
        has_status = self.status_get(status_name)
        for touching_cell in self.cellmap.area_get_cross(*self.location)[1:]:
            if not touching_cell:
                continue
            distance_to_no_status = 0
            if touching_cell.status_get(status_name):
                distance_to_no_status += 1
            tx, ty = touching_cell.location
            cx, cy = self.location
            direction = (tx - cx, ty - cy)
            next_cell_location = (tx + direction[0], ty + direction[1])
            further_cell = self.cellmap.cell_get(*next_cell_location)
            if further_cell:
                while further_cell.status_get(status_name):
                    distance_to_no_status += 1
                    fx, fy = further_cell.location
                    even_further_cell_location = (fx + direction[0], fy + direction[1])
                    further_cell = self.cellmap.cell_get(*even_further_cell_location)
                    if not further_cell:
                        break
                distances_to_no_status.append(distance_to_no_status)
        if distances_to_no_status:
            status_count = min(distances_to_no_status)
        else:
            status_count = 0
        if has_status:
            has_status.count = status_count
        return status_count

    def habitability(self, germ):
        surpluses = []
        for r in germ.required_resources:
            required_amount = germ.required_resources[r]
            current_amount = self.status_quality_amount(r)
            if current_amount < required_amount:
                return -1
            pct_surplus = (current_amount - required_amount) / float(required_amount)
            surpluses.append(pct_surplus)
        return sum(surpluses) / len(surpluses)

    def sweat(self):
        if self.terrain and self.terrain.name == "hair":
            will_sweat = not randint(0, 15)
        elif self.status_amount("wound") <= 1.0:
            will_sweat = not randint(0, 220)
        else:
            will_sweat = False
        if will_sweat:
            self.status_add("sweat")
        if self.terrain and self.terrain.name == "gland":
            if not randint(0, 5):
                excretion_field = self.cellmap.area_get_cross(*self.location)
                for tile in excretion_field:
                    if tile is None:
                        continue
                    if "sebum" in tile.statuses:
                        continue
                    tile.status_add("sebum")
                    break

    def sweat_evaporate(self):
        # if self.status_percentage("wet") > CALCULATED_MOISTURE_TENDENCY:
        if not randint(0, 4):
            self.status_add("sweat", amt=-1)

    def info_list(self):
        info = ["A patch of skin. It's about {0} degrees.".format(self.temperature)]
        for t in filter(lambda x: x, (self.terrain, self.flora)):
            info.append(t.name)
        for s in self.statuses:
            info.append((s + ' ' + str(self.statuses[s].amount)))
            info.append((s + ' ' + str(self.nearby_status_count(self.statuses[s].name))))
        for touching_cell in self.cellmap.area_get_cross(*self.location):
            if not touching_cell:
                continue
            info.append((str(touching_cell.location) + ', ' + str(self.location)))
        info.append(("integrity: " + str(self.integrity)))
        info.append(("perfusion: " + str(self.perfusion)))
        info.append(("moisture: " + str(self.moisture)))
        info.append(("temperature: " + str(self.temperature)))
        return info

    def tick(self):
        self.sweat()
        self.sweat_evaporate()

    def update(self):
        # self.dry(heatmap, exposedmap)
        # self.break_out()
        # self.heal()
        # etc
        for s in self.statuses.values():
            if s.amount <= 0:
                del self.statuses[s.name]
            self.nearby_status_count(s.name)


class CellMap(object):
    hud_location = (50, 0)

    def __init__(self, w, h, cons):
        self.w, self.h = w, h
        self.cell_con = cons["background"]
        self.fluids_con = cons["fluids"]
        self.hud_con = cons["hud"]
        self.cells = [None] * self.size
        self.cursor = None
        for x in range(w):
            for y in range(h):
                self.cell_add(x, y, SkinCell(self, choice(colors.LIGHT_SKIN_TONES)))
        self.random_setup()
        self.map_mode = None

    @property
    def size(self):
        return self.w * self.h

    def cell_add(self, x, y, cell):
        i = tools.xy_to_index(x, y, self.w)
        self.cells[i] = cell
        cell.location = (x, y)

    def random_setup(self):
        for c in self.cells:
            if not randint(0, 200):
                if not randint(0, 1):
                    c.flora = disease.Malassezia()
                else:
                    c.flora = disease.StaphAureus()
            if not randint(0, 15):
                if randint(0, 10):
                    c.terrain = terrain.HairFollicle()
                else:
                    c.terrain = terrain.SebaceousGland()


    def cell_remove(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        self.cells[i] = None

    def cell_get(self, x, y):
        i = tools.xy_to_index(x, y, self.w)
        try:
            return self.cells[i]
        except IndexError:
            return None

    def area_get_cross(self, x, y):
        a = [self.cell_get(cx, cy) for (cx, cy) in tools.generate_Z2(limit=1, origin=(x, y))]
        # a = [self.cell_get(cx, cy) for (cx, cy) in [(x + p[0], y + p[1]) for p in tools.CIRCLE_RANGE_1]]
        return a

    #  def cell_find_status(self, ox, oy, status_type,

    #    def evaporate(self):
    #        sweat_cells = filter(lambda x: x.status_get("sweat"), self.cells)
    #        if len(sweat_cells)/len(self.cells)

    def cell_bg_color(self, x, y):
        cell = self.cell_get(x, y)
        map_mode = map_modes.current_map_mode
        if map_mode:
            if map_mode.stat == "perfusion" or map_mode.stat == "integrity":
                stat_to_view = getattr(cell, map_mode.stat)
            elif map_mode.stat == "moisture":
                stat_to_view = getattr(cell, "moisture_scaled")
            elif map_mode.stat == "temperature":
                stat_to_view = getattr(cell, "temperature_scaled")
            else:
                raise NotImplementedError("Add your stat to the bgcolor logic!")
            return map_mode.color_map[int(stat_to_view * map_mode.num_color_indexes)]
        else:
            return cell.color

    def draw(self):
        for i, c in enumerate(self.cells):
            x, y = tools.index_to_xy(i, self.w)
            bgcolor = self.cell_bg_color(x, y)
            fgcolor = (c.terrain.color if c.terrain else libtcod.black)
            char = c.char
            #            x, y = self.game.camera.to_camera_coordinates(c.x, c.y)
            libtcod.console_set_char_background(self.cell_con, x, y, bgcolor)
            libtcod.console_set_default_foreground(self.cell_con, fgcolor)
            libtcod.console_put_char(self.cell_con, x, y,
                                     char, libtcod.BKGND_NONE)
            if c.statuses or c.flora:
                if c.statuses:
                    for s in c.statuses.values():
                        bgcolor = s.get_bgcolor()
                        wound_char = s.get_char()
                        if wound_char:
                            char = wound_char

                if c.flora:
                    char = c.flora.char
                    fgcolor = c.flora.color
                    bgcolor = libtcod.color_lerp(bgcolor, c.flora.bgcolor, .5)
                #                        libtcod.console_set_char_background(self.fluids_con, x, y, bgcolor)
                libtcod.console_set_char_background(self.fluids_con, x, y, bgcolor)
                libtcod.console_set_default_foreground(self.fluids_con, fgcolor)
                libtcod.console_put_char(self.fluids_con, x, y,
                                         char, libtcod.BKGND_NONE)
            else:
                libtcod.console_set_char_background(self.fluids_con, x, y, libtcod.black)

        if map_modes.current_map_mode:
            x, y = 0, 49
            for j, c in enumerate(map_modes.current_map_mode.stat.upper()):
                libtcod.console_put_char(self.hud_con, x + j, y,
                                         c, libtcod.BKGND_NONE)

        if self.cursor:
            x, y, char = self.cursor.x, self.cursor.y, self.cursor.char
            libtcod.console_set_default_foreground(self.hud_con, libtcod.dark_sepia)
            libtcod.console_put_char(self.hud_con, x, y,
                                     char, libtcod.BKGND_NONE)

            selected_tile = self.cell_get(self.cursor.x, self.cursor.y)
            if selected_tile:
                libtcod.console_set_default_foreground(self.hud_con, libtcod.dark_red)  # selected_tile.color)
                for j, item in enumerate(selected_tile.info_list()):
                    for i, c in enumerate(item):
                        if c is ' ':
                            c = '.'
                        x, y = self.hud_location[0] + i, self.hud_location[1] + j
                        libtcod.console_put_char(self.hud_con, x, y,
                                                 c, libtcod.BKGND_NONE)

    def update(self):
        for c in filter(lambda x: x, self.cells):
            c.update()
