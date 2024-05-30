import random

map_width = 45
map_height = 45
room_min_size = 8
room_max_size = 12
map_padding = 2  # 맵 바깥 경계 타일 개수
room_min_padding = 1  # 룸 최소 내부 간격
room_max_padding = 1  # 룸 최대 내부 간격
merge_room_max_gap = 3  # 룸 연결 기준

dungeon_map = [['.' for _ in range(map_width)] for _ in range(map_height)]
room_list = []
room_gen_id = 1


class Room:

  def __init__(self, x1, y1, x2, y2):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2


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


def generate_room(dungeon_map, x1, y1, x2, y2):
  global room_list, room_gen_id
  padding = random.randint(room_min_padding, room_max_padding)
  for y in range(y1 + padding, y2 - padding):
    for x in range(x1 + padding, x2 - padding):
      dungeon_map[y][x] = room_gen_id
  room_list.append(Room(x1, y1, x2, y2))
  room_gen_id += 1


def generate_map(dungeon_map, x1, y1, x2, y2):
  room_width = x2 - x1
  room_height = y2 - y1

  if (room_width < room_min_size or room_height < room_min_size):
    return

  if (room_width <= room_max_size and room_height <= room_max_size
      and random.random() < define_separator_per(x1, y1, x2, y2)):
    generate_room(dungeon_map, x1, y1, x2, y2)
    return

  if (random.random() < 0.5
      if room_width == room_height else room_height < room_width):
    cx = define_separator(x1, x2)
    generate_map(dungeon_map, x1, y1, cx, y2)
    generate_map(dungeon_map, cx, y1, x2, y2)
  else:
    cy = define_separator(y1, y2)
    generate_map(dungeon_map, x1, y1, x2, cy)
    generate_map(dungeon_map, x1, cy, x2, y2)


def make_corridor(dungeon_map, room_list):
  for i in range(len(room_list) - 1):
    r1, r2 = room_list[i], room_list[i + 1]
    cx1, cy1 = (r1.x1 + r1.x2) // 2, (r1.y1 + r1.y2) // 2
    cx2, cy2 = (r2.x1 + r2.x2) // 2, (r2.y1 + r2.y2) // 2

    for x in range(cx1, cx2):
      dungeon_map[cy1][x] = 0
      dungeon_map[cy2][x] = 0
    for y in range(cy1, cy2):
      dungeon_map[y][cx1] = 0
      dungeon_map[y][cx2] = 0


def print_map(dungeon_map):
  for row in dungeon_map:
    print(" ".join(map(str, row)))


generate_map(dungeon_map, map_padding, map_padding, map_width - map_padding,
             map_height - map_padding)
make_corridor(dungeon_map, room_list)
print_map(dungeon_map)
