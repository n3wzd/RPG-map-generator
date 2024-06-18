import random
from collections import deque

import tile_rule as tile

# Parameter
map_width = 45
map_height = 45
room_min_size = 10
room_max_size = 18
map_padding = 2  # min = 1
room_min_padding = 1
room_max_padding = 1
corridor_wide = 2
wall_height = 2

# Constant
MAX_LAYER = 5

# Map Index
# 0 = Base Tile 1
# 1 = Base Tile 2
# 2 = Deco Tile 1
# 3 = Deco Tile 2
# 4 = Shadow Tile
# 5 = Restrict ID (Not Used)

theme = {
    tile.blank: 1536,
    tile.floor: 2816,
    tile.wall: 6274,
    tile.ceil: 5888,
}


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
    self.map_basic = [[[0 for _ in range(2)] for _ in range(map_width)]
                      for _ in range(map_height)]
    self.room_graph = []
    self.room_list = []
    self.generate_dungeon()

  def generate_dungeon(self):
    mp = map_padding
    self.generate_map(mp, mp, map_width - mp, map_height - mp)
    self.generate_graph()
    self.connect_rooms()
    self.place_ceil()
    self.define_tile_id()
    # self.place_decorations(3)

  def generate_map(self, x1, y1, x2, y2):
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

  def generate_graph(self):
    R = self.room_list
    self.room_graph = [[0 for _ in range(len(R))] for _ in range(len(R))]

    for i in range(len(R)):
      for j in range(len(R)):
        if i != j:
          dist = rect_distance(R[i], R[j])
          self.room_graph[j][i] = self.room_graph[i][j] = dist

  def connect_rooms(self):
    dist = self.room_graph
    min_dist = floyd_warshall(self.room_graph)

    for i in range(len(dist)):
      for j in range(i + 1, len(dist)):
        if dist[i][j] == min_dist[i][j]:
          self.make_corridor(i, j)

  def make_corridor(self, i, j):
    cw, wh = corridor_wide, wall_height
    r1, r2 = self.room_list[i], self.room_list[j]
    cx1 = random.randrange(r1.x1 + cw, r1.x2 - cw)
    cy1 = random.randrange(r1.y1 + cw + wh, r1.y2 - cw)
    cx2 = random.randrange(r2.x1 + cw, r2.x2 - cw)
    cy2 = random.randrange(r2.y1 + cw + wh, r2.y2 - cw)
    dire = random.randint(0, 1)

    for x in range(min(cx1, cx2 + 1) - cw, max(cx1, cx2 + 1) + cw):
      by = cy1 if dire == 0 else cy2
      for y in range(by - cw - wh, by + cw + 1):
        self.map_basic[y][x][0] = tile.floor
    for y in range(min(cy1, cy2 + 1) - cw - wh, max(cy1, cy2 + 1) + cw):
      bx = cx2 if dire == 0 else cx1
      for x in range(bx - cw, bx + cw + 1):
        self.map_basic[y][x][0] = tile.floor

  def place_ceil(self):
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
      self.place_wall(x, y)

  def place_wall(self, x, y):
    if self.map_basic[y + 1][x][0] == tile.floor:
      for dy in range(1, wall_height + 1):
        self.map_basic[y + dy][x][0] = tile.wall

  def define_tile_id(self):
    for y in range(map_height):
      for x in range(map_width):
        for r in range(2):
          target = self.map_basic[y][x][r]
          self.map[y][x][r] = theme[target]
          if (target == tile.floor or target == tile.ceil):
            self.map[y][x][r] += self.interpolate_floor_tile(x, y, r)

  def interpolate_floor_tile(self, x, y, r):
    dmap = [[0 for _ in range(3)] for _ in range(3)]
    for dy in range(3):
      for dx in range(3):
        nx, ny = x + dx - 1, y + dy - 1
        dmap[dy][dx] = (1 if self.map_basic[y][x][r]
                        == self.map_basic[ny][nx][r] else 0)

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

  """
  def get_tiles_by_neighbors(self, x, y):
    tiles = []
    for dy in [-1, 0, 1]:
      for dx in [-1, 0, 1]:
        nx, ny = x + dx, y + dy
        for cond in tile.data_prob.get(self.map_basic[ny][nx][0], {}).get(
            (dx, dy), []):
          if (random.random() < cond.prob
              and cond.target in tile.data_base.get(self.map_basic[y][x][0],
                                                    set())):
            tiles.append(cond)
    return tiles

  def place_deco(self, x, y, target):
    group = tile.data_group.get(target, [])
    ok = True
    for member in group:
      nx, ny = (x + member.dx, y + member.dy)
      ok = ok and member.target in tile.data_base.get(
          self.map_basic[ny][nx][0], set())

    if ok:
      self.map_basic[y][x][0] = target
      for member in group:
        nx, ny = (x + member.dx, y + member.dy)
        self.map_basic[ny][nx][0] = member.target

  def place_decorations(self, iter):
    pd = map_padding
    for _ in range(iter):
      for y in range(pd, map_height - pd):
        for x in range(pd, map_width - pd):
          list = self.get_tiles_by_neighbors(x, y)
          if len(list) > 0:
            list.sort(key=lambda cond: cond.prob, reverse=True)
            self.place_deco(x, y, list[0].target)
  """


def rect_distance(a, b):
  x_dist = max(0, b.x1 - a.x2, a.x1 - b.x2)
  y_dist = max(0, b.y1 - a.y2, a.y1 - b.y2)

  if x_dist == 0:
    return y_dist
  elif y_dist == 0:
    return x_dist
  else:
    return x_dist + y_dist + 1


def floyd_warshall(graph):
  n = len(graph)
  dist = [row[:] for row in graph]

  for k in range(n):
    for i in range(n):
      for j in range(n):
        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

  return dist


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

def main():
  return Dungeon()
