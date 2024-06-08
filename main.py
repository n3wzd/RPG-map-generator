import random
from collections import deque
import module

# 파라미터
map_width = 45
map_height = 45
room_min_size = 10
room_max_size = 18
map_padding = 2  # 맵 바깥 경계 타일 개수 (최소값 1)
room_min_padding = 1  # 룸 최소 내부 간격
room_max_padding = 1  # 룸 최대 내부 간격
corridor_wide = 2  # 통로 너비
wall_height = 2  # 벽 높이

# 타일 종류
tile_floor = module.Tile('0')
tile_wall = module.Tile('1')
tile_ceil = module.Tile('2')
tile_floor_deco = [
    module.Tile('A', 0.1, [module.TileCondition('B', (0, -1), 1.0)]),
    module.Tile('B', 0.1, [module.TileCondition('A', (0, 1), 1.0)]),
    module.Tile('C', 0.2, [
        module.TileCondition('1', (1, 0), 0.75),
        module.TileCondition('1', (-1, 0), 0.75),
        module.TileCondition('1', (0, 1), 0.75),
        module.TileCondition('1', (0, -1), 0.75)
    ]),
    module.Tile('D', 0.15),
]
tile_wall_deco = [
    module.Tile('E', 0.25),
]


class Dungeon:

  def __init__(self):
    self.map = [['.' for _ in range(map_width)] for _ in range(map_height)]
    self.room_graph = []
    self.room_list = []

  def generate_room(self, x1, y1, x2, y2):
    padding = random.randint(room_min_padding, room_max_padding)
    x1 += padding
    x2 -= padding
    y1 += padding
    y2 -= padding

    room = module.Room(x1, y1, x2, y2, len(self.room_list))
    for y in range(y1, y2):
      for x in range(x1, x2):
        self.map[y][x] = str(0)
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
        self.map[y][x] = tile_floor.id
    for y in range(min(cy1, cy2 + 1) - cw - wh, max(cy1, cy2 + 1) + cw):
      bx = cx2 if dire == 0 else cx1
      for x in range(bx - cw, bx + cw + 1):
        self.map[y][x] = tile_floor.id

  def make_ceil(self):
    r = self.room_list[0]
    visited = set()
    queue = deque([(r.x1, r.y1)])
    visited.add((r.x1, r.y1))
    dire = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1),
            (-1, 1)]
    ceil_set = set()

    while queue:
      x, y = queue.popleft()
      isCeil = False

      for d in dire:
        nx, ny = x + d[0], y + d[1]
        nv = self.map[ny][nx]
        isCeil = isCeil or nv == '.'

        if (nx, ny) not in visited and nv != '.':
          visited.add((nx, ny))
          queue.append((nx, ny))

      if isCeil:
        self.map[y][x] = tile_ceil.id
        ceil_set.add((x, y))

    for x, y in ceil_set:
      self.make_wall(x, y)

  def make_wall(self, x, y):
    if self.map[y + 1][x] == tile_floor.id:
      for dy in range(1, wall_height + 1):
        self.map[y + dy][x] = tile_wall.id

  def count_neighbors(self, x, y, target):
    count = 0
    for dy in [-1, 0, 1]:
      for dx in [-1, 0, 1]:
        if dx == 0 and dy == 0:
          continue
        if self.map[y + dy][x + dx] == target:
          count += 1
    return count

  def place_decorations(self, tile):
    pd = map_padding
    for y in range(pd, map_height - pd):
      for x in range(pd, map_width - pd):
        if self.map[y][x] == tile_floor.id and random.random(
        ) < tile.init_prob:
          self.map[y][x] = tile.id

  def print_map(self):
    for row in self.map:
      print(" ".join(map(str, row)))


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


def generate_map(dungeon, x1, y1, x2, y2):
  room_width = x2 - x1
  room_height = y2 - y1

  if (room_width < room_min_size or room_height < room_min_size):
    return

  if (room_width <= room_max_size and room_height <= room_max_size
      and random.random() < define_separator_per(x1, y1, x2, y2)):
    dungeon.generate_room(x1, y1, x2, y2)
    return

  if (random.random() < 0.5
      if room_width == room_height else room_height < room_width):
    cx = define_separator(x1, x2)
    generate_map(dungeon, x1, y1, cx, y2)
    generate_map(dungeon, cx, y1, x2, y2)
  else:
    cy = define_separator(y1, y2)
    generate_map(dungeon, x1, y1, x2, cy)
    generate_map(dungeon, x1, cy, x2, y2)


def main():
  mp = map_padding
  dungeon = Dungeon()
  generate_map(dungeon, mp, mp, map_width - mp, map_height - mp)
  dungeon.generate_graph()
  dungeon.connect_rooms()
  dungeon.make_ceil()
  for tile in tile_floor_deco:
    dungeon.place_decorations(tile)
  dungeon.print_map()


main()
