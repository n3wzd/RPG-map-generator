import random
from collections import deque

import parameter as param
import tile_rule as tile

map_width = param.map_width
map_height = param.map_height
room_min_size = param.room_min_size
room_max_size = param.room_max_size
map_padding = param.map_padding
room_min_padding = param.room_min_padding
room_max_padding = param.room_max_padding
corridor_wide_auto = param.corridor_wide_auto
corridor_wide = param.corridor_wide
wall_height = param.wall_height
MAX_LAYER = 6


class Room:

  def __init__(self, x1, y1, x2, y2, id):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.id = id


class Dungeon:

  def __init__(self):
    self.map = [[[0 for _ in range(MAX_LAYER)] for _ in range(map_width)]
                for _ in range(map_height)]
    self.map_basic = [[[tile.blank, tile.transparent]
                       for _ in range(map_width)] for _ in range(map_height)]
    self.room_graph = []
    self.room_list = []
    self.generate_dungeon()

  def generate_dungeon(self):
    mp = map_padding
    self.generate_map(mp, mp, map_width - mp, map_height - mp)
    self.generate_graph()
    self.connect_rooms()
    self.place_wall_ceil()
    self.place_area_all()
    self.place_cascade_all()
    self.place_decorations()
    self.place_shadows()
    self.define_tile_id()

  def generate_map(self, x1, y1, x2, y2):

    def define_separator(a, b):
      d = room_min_size
      p, q = a + d, b - d
      if p <= q:
        return random.randint(a + 1, b - 1)
      else:
        r = random.randint(1, b - a - d)
        return random.choice([a + r, b - r])

    def define_separator_per(x1, y1, x2, y2):
      d = room_min_size
      a, b = (x1, x2) if (y2 - y1) < (x2 - x1) else (y1, y2)

      if b - a == d:
        return 1

      p, q = a + d, b - d
      return 1 / (b - a) if p <= q else 1 / (b - a - d) * 2

    room_width = x2 - x1
    room_height = y2 - y1

    if (room_width < room_min_size or room_height < room_min_size):
      return

    if (room_width <= room_max_size and room_height <= room_max_size
        and random.random() < define_separator_per(x1, y1, x2, y2)):
      self.generate_room(x1, y1, x2, y2)
      return

    if (random.random() < 0.5
        if room_width == room_height else room_height < room_width):
      cx = define_separator(x1, x2)
      self.generate_map(x1, y1, cx, y2)
      self.generate_map(cx, y1, x2, y2)
    else:
      cy = define_separator(y1, y2)
      self.generate_map(x1, y1, x2, cy)
      self.generate_map(x1, cy, x2, y2)

  def generate_graph(self):

    def rect_distance(a, b):
      x_dist = max(0, b.x1 - a.x2, a.x1 - b.x2)
      y_dist = max(0, b.y1 - a.y2, a.y1 - b.y2)

      if x_dist == 0:
        return y_dist
      elif y_dist == 0:
        return x_dist
      else:
        return x_dist + y_dist + 1

    R = self.room_list
    self.room_graph = [[0 for _ in range(len(R))] for _ in range(len(R))]

    for i in range(len(R)):
      for j in range(len(R)):
        if i != j:
          dist = rect_distance(R[i], R[j])
          self.room_graph[j][i] = self.room_graph[i][j] = dist

  def generate_room(self, x1, y1, x2, y2):
    padding = random.randint(room_min_padding, room_max_padding)
    x1 += padding
    x2 -= padding
    y1 += padding
    y2 -= padding

    room = Room(x1, y1, x2, y2, len(self.room_list))
    for y in range(y1, y2):
      for x in range(x1, x2):
        self.map_basic[y][x][0] = tile.floor
    self.room_list.append(room)

  def connect_rooms(self):

    def floyd_warshall(graph):
      n = len(graph)
      dist = [row[:] for row in graph]

      for k in range(n):
        for i in range(n):
          for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

      return dist

    def make_corridor(i, j):
      r1, r2 = self.room_list[i], self.room_list[j]
      dire = random.randint(0, 1)

      if corridor_wide_auto:
        for x in range(min(r1.x1, r2.x1), max(r1.x2, r2.x2) + 1):
          ry = (r1.y1, r1.y2) if dire == 0 else (r2.y1, r2.y2)
          for y in range(ry[0], ry[1] + 1):
            self.map_basic[y][x][0] = tile.floor
        for y in range(min(r1.y1, r2.y1), max(r1.y2, r2.y2) + 1):
          rx = (r2.x1, r2.x2) if dire == 0 else (r1.x1, r1.x2)
          for x in range(rx[0], rx[1] + 1):
            self.map_basic[y][x][0] = tile.floor
      else:
        cw, wh = corridor_wide, wall_height
        cx1 = random.randrange(r1.x1 + cw, r1.x2 - cw)
        cy1 = random.randrange(r1.y1 + cw + wh, r1.y2 - cw)
        cx2 = random.randrange(r2.x1 + cw, r2.x2 - cw)
        cy2 = random.randrange(r2.y1 + cw + wh, r2.y2 - cw)

        for x in range(min(cx1, cx2 + 1) - cw, max(cx1, cx2 + 1) + cw):
          by = cy1 if dire == 0 else cy2
          for y in range(by - cw - wh, by + cw + 1):
            self.map_basic[y][x][0] = tile.floor
        for y in range(min(cy1, cy2 + 1) - cw - wh, max(cy1, cy2 + 1) + cw):
          bx = cx2 if dire == 0 else cx1
          for x in range(bx - cw, bx + cw + 1):
            self.map_basic[y][x][0] = tile.floor

    dist = self.room_graph
    min_dist = floyd_warshall(self.room_graph)

    for i in range(len(dist)):
      for j in range(i + 1, len(dist)):
        if dist[i][j] == min_dist[i][j]:
          make_corridor(i, j)

  def place_wall_ceil(self):

    def place_wall(x, y):
      if (y < map_height - wall_height
          and self.map_basic[y + 1][x][0] == tile.floor):
        for dy in range(1, wall_height + 1):
          self.map_basic[y + dy][x][0] = tile.wall

    start = self.room_list[0]
    visited = set()
    queue = deque([(start.x1, start.y1)])
    visited.add((start.x1, start.y1))
    dire = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1),
            (-1, 1)]
    ceil_set = set()

    while queue:
      x, y = queue.popleft()
      isCeil = False

      for d in dire:
        nx, ny = x + d[0], y + d[1]
        nv = self.map_basic[ny][nx][0]
        isCeil = isCeil or nv == tile.blank

        if (nx, ny) not in visited and nv != tile.blank:
          visited.add((nx, ny))
          queue.append((nx, ny))

      if isCeil:
        self.map_basic[y][x][0] = tile.ceil
        ceil_set.add((x, y))

    for x, y in ceil_set:
      place_wall(x, y)

  def place_area(self, area_tile, base_id, layer):
    (CAP_MIN, CAP_MAX) = (area_tile.capacity_min, area_tile.capacity_max)
    target = area_tile.id
    pd = map_padding
    dire = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    class AreaSeed:

      def __init__(self, x, y, direction, magnitude, capacity):

        def get_prob():
          prob = []
          for i in range(4):
            diff = abs(direction - i * 90)
            d = min(diff, 360 - diff) / 180
            r = magnitude
            prob.append(((1 - r) * 0.5 + r * (1 - d)) * 0.5)
          return prob

        self.pos = (x, y)
        self.prob = get_prob()
        self.capacity = capacity

    def create_seed():
      seed_list = []
      for y in range(pd, map_height - pd):
        for x in range(pd, map_width - pd):
          if (self.map_basic[y][x][0] == base_id
              and random.random() < area_tile.seed_gen_rate):
            seed_list.append(
                AreaSeed(x, y,
                         random.random() * 360, random.random(),
                         random.randint(CAP_MIN, CAP_MAX)))
      return seed_list

    def spread(seed):
      self.map_basic[seed.pos[1]][seed.pos[0]][layer] = target
      buffer = {seed.pos}

      for _ in range(seed.capacity):
        iter_buffer = buffer.copy()
        for v in iter_buffer:
          flag = True
          for i in range(4):
            (x, y) = v[0] + dire[i][0], v[1] + dire[i][1]
            flag = flag and self.map_basic[y][x][0] != base_id

          if flag:
            buffer.remove(v)
          else:
            for i in range(4):
              (x, y) = v[0] + dire[i][0], v[1] + dire[i][1]
              if (self.map_basic[y][x][0] == base_id
                  and random.random() < seed.prob[i]):
                buffer.add((x, y))
                self.map_basic[y][x][layer] = target

    def trim():

      def clean_out(x, y):
        if self.map_basic[y][x][layer] == target:
          flag = 0
          for d in dire:
            nx, ny = x + d[0], y + d[1]
            flag += 1 if self.map_basic[ny][nx][layer] != target else 0
          if flag >= 3:
            if layer == 0:
              self.map_basic[y][x][layer] = base_id
            else:
              self.map_basic[y][x][layer] = 0
            for d in dire:
              clean_out(x + d[0], y + d[1])

      def fill(x, y):
        if self.map_basic[y][x][0] == base_id:
          flag = True
          for d in dire:
            (nx, ny) = x + d[0], y + d[1]
            flag = flag and self.map_basic[ny][nx][layer] == target

          if flag:
            self.map_basic[y][x][layer] = target

      for y in range(pd, map_height - pd):
        for x in range(pd, map_width - pd):
          clean_out(x, y)

      for y in range(pd, map_height - pd):
        for x in range(pd, map_width - pd):
          fill(x, y)

    def place_carpet():

      def create_square(x1, y1, x2, y2):
        if x1 < 0 or y1 < 0 or x2 >= map_width or y2 >= map_height:
          return

        ok = True
        for y in range(y1, y2 + 1):
          for x in range(x1, x2 + 1):
            ok = ok and self.map_basic[y][x][0] == base_id
            if layer == 1:
              ok = ok and self.map_basic[y][x][layer] == 0

        if ok:
          for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
              self.map_basic[y][x][layer] = target

      for room in self.room_list:

        def diagonal_search(sx, sy, d, iter):
          dire = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
          x, y = sx, sy
          for _ in range(iter):
            if random.random() < area_tile.seed_gen_rate:
              lx = random.randint(CAP_MIN, CAP_MAX)
              ly = random.randint(CAP_MIN, CAP_MAX)
              if d == 0:
                create_square(x, y, x + lx, y + ly)
              if d == 1:
                create_square(x - lx, y, x, y + ly)
              if d == 2:
                create_square(x, y - ly, x + lx, y)
              if d == 3:
                create_square(x - lx, y - ly, x, y)

            x += dire[d][0]
            y += dire[d][1]

        x1, y1 = room.x1 + 1, room.y1 + wall_height + 1
        x2, y2 = room.x2 - 2, room.y2 - 2
        iter = min((x1 + x2) // 2, (y1 + y2) // 2)
        plist = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]

        for i in range(4):
          diagonal_search(plist[i][0], plist[i][1], i, iter)

    if area_tile.carpet:
      place_carpet()
    else:
      seed_list = create_seed()
      for seed in seed_list:
        spread(seed)
      trim()

  def place_area_all(self):
    for tx in tile.extra:
      self.place_area(tx.base, tile.floor, 0)
    for tx in tile.floor_cover:
      self.place_area(tx, tile.floor, 1)
    for tx in tile.extra:
      for cx in tx.coverList:
        self.place_area(cx, tx.base.id, 1)

  def place_cascade(self, area_tile_set):

    def extend_cascade(px, py):
      x, y = px, py
      while y >= 0 and self.map_basic[y][x][0] == tile.wall:
        self.map_basic[y][x][0] = cascade_id
        y -= 1

    pd = map_padding
    base_id = area_tile_set.base.id
    cascade_id = area_tile_set.cascade.id
    gen_rate = area_tile_set.cascade.seed_gen_rate
    wide_min = area_tile_set.cascade.wide_min
    wide_max = area_tile_set.cascade.wide_max

    for y in range(pd, map_height - pd):
      for x in range(pd, map_width - pd):
        if (self.map_basic[y][x][0] == base_id and y > 0
            and random.random() < gen_rate):
          wide = random.randint(wide_min, wide_max)
          flag = True
          for w in range(wide):
            if x + w < map_width:
              flag = (flag and self.map_basic[y - 1][x + w][0] == tile.wall
                      and self.map_basic[y][x + w][0] == base_id)
            else:
              flag = False
          flag = (flag and
                  (x - 1 == 0 or self.map_basic[y - 1][x - 1][0] == tile.wall))
          flag = (flag
                  and (x + wide == map_width
                       or self.map_basic[y - 1][x + wide][0] == tile.wall))
          if flag:
            for w in range(wide):
              extend_cascade(x + w, y - 1)

  def place_cascade_all(self):
    for tx in tile.extra:
      if tx.cascade is not None:
        self.place_cascade(tx)

  def define_tile_id(self):

    def interpolate_floor_tile(x, y, r):
      dmap = [[0 for _ in range(3)] for _ in range(3)]
      for dy in range(3):
        for dx in range(3):
          nx, ny = x + dx - 1, y + dy - 1
          cond = self.map_basic[y][x][r] == self.map_basic[ny][nx][r]
          if dy == 0:
            cond = (cond
                    or self.map_basic[ny][nx][r] in tile.TileCore.type_cascade)
          dmap[dy][dx] = 1 if cond else 0

      for i in range(len(tile.floor_automata)):
        automata = tile.floor_automata[i]
        ok = True
        for dy in range(3):
          for dx in range(3):
            if automata[dy][dx] == 2:
              continue
            ok = ok and dmap[dy][dx] == automata[dy][dx]
        if (ok):
          return i

      return 0

    def interpolate_wall_tile(x, y, r):

      def dist_tile(tx, ty, target):
        dist = 0
        while self.map_basic[ty - dist][tx][r] != target and ty - dist >= 0:
          dist += 1
        return dist

      dmap = [0] * 4
      dire = [(-1, 0), (0, -1), (1, 0), (0, 1)]
      for i in range(4):
        nx, ny = x + dire[i][0], y + dire[i][1]
        cond = (self.map_basic[y][x][r] == self.map_basic[ny][nx][r]
                or self.map_basic[ny][nx][r] in tile.TileCore.type_cascade)
        if dire[i][0] != 0:
          cond = cond and dist_tile(x, y, tile.ceil) == dist_tile(
              nx, ny, tile.ceil)
        dmap[i] = 1 if cond else 0

      for i in range(len(tile.wall_automata)):
        automata = tile.wall_automata[i]
        ok = True
        for j in range(4):
          ok = ok and dmap[j] == automata[j]
        if (ok):
          return i

      return 0

    def interpolate_cascade_tile(x, y, r):
      dmap = [0] * 2
      dire = [-1, 1]
      for i in range(2):
        nx = x + dire[i]
        cond = self.map_basic[y][x][r] == self.map_basic[y][nx][r]
        dmap[i] = 1 if cond else 0

      for i in range(len(tile.cascade_automata)):
        automata = tile.cascade_automata[i]
        ok = True
        for j in range(2):
          ok = ok and dmap[j] == automata[j]
        if (ok):
          return i

      return 0

    for y in range(map_height):
      for x in range(map_width):
        for r in range(2):
          target = self.map_basic[y][x][r]
          self.map[y][x][r] = param.theme[target]
          if (target in tile.TileCore.type_floor):
            self.map[y][x][r] += interpolate_floor_tile(x, y, r)
          elif (target in tile.TileCore.type_wall):
            self.map[y][x][r] += interpolate_wall_tile(x, y, r)
          elif (target in tile.TileCore.type_cascade):
            self.map[y][x][r] += interpolate_cascade_tile(x, y, r)

  def place_decorations(self):

    def check_adj_wall(x, y, cond):
      flag = True
      if cond.adj_wall[0]:
        flag = flag and self.map_basic[y - 1][x][0] == tile.wall
      if cond.adj_wall[1]:
        flag = flag and self.map_basic[y + 1][x][0] == tile.ceil
      if cond.adj_wall[2]:
        flag = flag and (self.map_basic[y][x + 1][0] == tile.ceil
                         or self.map_basic[y][x - 1][0] == tile.ceil)
      return flag

    def gen_deco_tiles(x, y):
      tiles = []
      tile_basic = self.map_basic[y][x][0]
      for cond in tile.gen_normal.get(tile_basic, []):
        if (self.map[y][x][tile.layer_data[cond.target]] == tile.transparent
            and random.random() < cond.prob and check_adj_wall(x, y, cond)):
          tiles.append(cond)
      return tiles

    def place_deco(x, y, target):
      group = tile.gen_group.get(target, [])
      ok = True
      for member in group:
        nx, ny = (x + member.dx, y + member.dy)
        ok = ok and self.map[ny][nx][tile.layer_data[
            member.target]] == tile.transparent
        if member.base_id != -2:
          tile_basic = (self.map_basic[y][x][0]
                        if member.base_id == -1 else member.base_id)
          ok = ok and self.map_basic[ny][nx][0] == tile_basic

      if ok:
        self.map[y][x][tile.layer_data[target]] = target
        for member in group:
          nx, ny = (x + member.dx, y + member.dy)
          self.map[ny][nx][tile.layer_data[member.target]] = member.target

    pd = map_padding
    for y in range(pd, map_height - pd):
      for x in range(pd, map_width - pd):
        list = gen_deco_tiles(x, y)
        if len(list) > 0:
          list.sort(key=lambda cond: cond.prob, reverse=True)
          place_deco(x, y, list[0].target)

  def place_shadows(self):
    pd = map_padding
    for y in range(pd, map_height - pd):
      for x in range(pd, map_width - pd):
        ut = self.map_basic[y - 1][x][0]
        lt = self.map_basic[y][x + 1][0]
        ct = self.map_basic[y][x][0]
        cond1 = (ut == tile.ceil or ut == tile.wall)
        cond2 = (lt != tile.ceil and lt != tile.wall
                 and lt not in tile.TileCore.type_cascade)
        cond3 = (ct == tile.ceil or ct == tile.wall)
        if cond1 and cond2 and cond3:
          self.map[y][x + 1][4] = 5


def main():
  return Dungeon()
