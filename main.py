import random

# 던전 맵 제너레이터

map_width = 30
map_height = 30
room_min_size = 4
room_max_size = 15
map_padding = 2  # 맵 바깥 경계 타일 개수
room_min_margin = 1  # 최소 룸 간격
room_max_margin = 1  # 최대 룸 간격

dungeon_map = [['.' for _ in range(map_width)] for _ in range(map_height)]
room_id_gen = 0


def generate_room(dungeon_map, x1, y1, x2, y2):
  global room_id_gen
  for y in range(y1, y2):
    for x in range(x1, x2):
      dungeon_map[y][x] = room_id_gen
  room_id_gen += 1


def define_center(a, b, diff):
  p = a + diff
  q = b - diff
  print(a, b, p, q, diff)
  if p <= q:
    return random.randint(p, q)
  else:
    return random.choice([random.randint(p, b - 1), random.randint(a + 1, q)])


def generate_map(dungeon_map, x1, y1, x2, y2):
  room_width = x2 - x1
  room_height = y2 - y1

  if (room_width <= room_min_size or room_height <= room_min_size):
    return

  if (room_width <= room_max_size and room_height <= room_max_size
      and random.random() < 1 / (room_width - room_min_size + 1)):
    generate_room(dungeon_map, x1, y1, x2, y2)
    return

  # room_margin = random.randint(room_min_margin, room_max_margin)
  if (random.random() < 0.5
      if room_width == room_height else room_height < room_width):
    cx = define_center(x1, x2, room_min_size)
    generate_map(dungeon_map, x1, y1, cx, y2)
    generate_map(dungeon_map, cx, y1, x2, y2)
  else:
    cy = define_center(y1, y2, room_min_size)
    generate_map(dungeon_map, x1, y1, x2, cy)
    generate_map(dungeon_map, x1, cy, x2, y2)


def print_map(dungeon_map):
  for row in dungeon_map:
    print(" ".join(map(str, row)))


generate_map(dungeon_map, map_padding, map_padding, map_width - map_padding,
             map_height - map_padding)
print_map(dungeon_map)
