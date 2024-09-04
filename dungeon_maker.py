import math
import random
import heapq
from collections import deque

import parameter as param
import tile_rule as tile


class RectArea:

  def __init__(self, x1, y1, x2, y2, id):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.id = id


class Dungeon:

  def __init__(self):
    self.map = [[[0 for _ in range(6)] for _ in range(param.map_width)]
                for _ in range(param.map_height)]
    self.bmap = [[[tile.blank, tile.transparent]
                  for _ in range(param.map_width)]
                 for _ in range(param.map_height)]
    self.hmap = [[0 for _ in range(param.map_width)]
                 for _ in range(param.map_height)]
    self.room_list = []  # only BSP
    self.generate_dungeon()

  def generate_dungeon(self):
    if 0 <= param.map_type <= 1:
      if param.map_type == 0:
        self.build_BSP()
      if param.map_type == 1:
        self.build_cellular_automata()
      self.place_wall()
      self.place_ceil()
    if param.map_type == 2:
      self.build_plain()
    if param.map_type == 3:
      self.build_perlin_noise()
    self.place_structure()
    self.place_area_all()
    self.place_cascade_all()
    self.place_decorations()
    self.place_shadows()
    self.define_tile_id()

  def rect_distance(self, a, b):
    x_dist = max(0, b.x1 - a.x2, a.x1 - b.x2)
    y_dist = max(0, b.y1 - a.y2, a.y1 - b.y2)

    if x_dist == 0:
      return y_dist
    elif y_dist == 0:
      return x_dist
    else:
      return x_dist + y_dist + 1

  def build_BSP(self):
    space_min_width = param.room_min_size + param.room_padding * 2 + 1
    space_max_width = param.room_max_size + param.room_padding * 2 + 1
    space_min_height = (param.room_min_size + param.room_padding * 2 +
                        param.wall_height + 1)
    space_max_height = (param.room_max_size + param.room_padding * 2 +
                        param.wall_height + 1)

    def generate_map(x1, y1, x2, y2):

      def define_separator(a, b, is_y):
        d = space_min_height if is_y else space_min_width
        p, q = a + d, b - d
        if p <= q:
          return random.randint(a + 1, b - 1)
        else:
          r = random.randint(1, b - a - d)
          return random.choice([a + r, b - r])

      def define_separator_per(x1, y1, x2, y2):
        d = space_min_width
        a, b = (x1, x2) if (y2 - y1) < (x2 - x1) else (y1, y2)

        if b - a == d:
          return 1

        p, q = a + d, b - d
        return 1 / (b - a) if p <= q else 1 / (b - a - d) * 2

      space_width = x2 - x1
      space_height = y2 - y1

      if (space_width < space_min_width or space_height < space_min_height):
        return

      if (space_width <= space_max_width and space_height <= space_max_height
          and random.random() < define_separator_per(x1, y1, x2, y2)
          and random.random() < param.room_freq):
        generate_room(x1, y1, x2, y2)
        return

      if (space_width == space_min_width or space_height == space_min_height):
        return

      if (random.random() < 0.5
          if space_width == space_height else space_height < space_width):
        cx = define_separator(x1, x2, False)
        generate_map(x1, y1, cx, y2)
        generate_map(cx, y1, x2, y2)
      else:
        cy = define_separator(y1, y2, True)
        generate_map(x1, y1, x2, cy)
        generate_map(x1, cy, x2, y2)

    def generate_graph():
      R = self.room_list
      room_graph = [[0 for _ in range(len(R))] for _ in range(len(R))]

      for i in range(len(R)):
        for j in range(len(R)):
          if i != j:
            dist = self.rect_distance(R[i], R[j])
            room_graph[j][i] = room_graph[i][j] = dist

      return room_graph

    def generate_room(x1, y1, x2, y2):
      padding = param.room_padding + 1
      x1 += padding
      x2 -= padding
      y1 += padding + param.wall_height
      y2 -= padding

      room = RectArea(x1, y1, x2, y2, len(self.room_list))
      for y in range(y1, y2):
        for x in range(x1, x2):
          self.bmap[y][x][0] = tile.floor
      self.room_list.append(room)

    def connect_rooms(room_graph):

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

        if param.corridor_wide_auto:
          for x in range(min(r1.x1, r2.x1), max(r1.x2, r2.x2) + 1):
            ry = (r1.y1, r1.y2) if dire == 0 else (r2.y1, r2.y2)
            for y in range(ry[0], ry[1] + 1):
              self.bmap[y][x][0] = tile.floor
          for y in range(min(r1.y1, r2.y1), max(r1.y2, r2.y2) + 1):
            rx = (r2.x1, r2.x2) if dire == 0 else (r1.x1, r1.x2)
            for x in range(rx[0], rx[1] + 1):
              self.bmap[y][x][0] = tile.floor
        else:
          cw = param.corridor_wide
          cx1 = random.randrange(r1.x1 + cw, r1.x2 - cw)
          cy1 = random.randrange(r1.y1 + cw, r1.y2 - cw)
          cx2 = random.randrange(r2.x1 + cw, r2.x2 - cw)
          cy2 = random.randrange(r2.y1 + cw, r2.y2 - cw)

          for x in range(min(cx1, cx2 + 1) - cw, max(cx1, cx2 + 1) + cw):
            by = cy1 if dire == 0 else cy2
            for y in range(by - cw, by + cw + 1):
              self.bmap[y][x][0] = tile.floor
          for y in range(min(cy1, cy2 + 1) - cw, max(cy1, cy2 + 1) + cw):
            bx = cx2 if dire == 0 else cx1
            for x in range(bx - cw, bx + cw + 1):
              self.bmap[y][x][0] = tile.floor

      dist = room_graph
      min_dist = floyd_warshall(room_graph)

      for i in range(len(dist)):
        for j in range(i + 1, len(dist)):
          if dist[i][j] == min_dist[i][j]:
            make_corridor(i, j)

    mp = param.map_padding
    generate_map(mp, mp, param.map_width - mp, param.map_height - mp)
    room_graph = generate_graph()
    connect_rooms(room_graph)

  def build_cellular_automata(self):
    mp = param.map_padding + 1

    def initialize():
      for y in range(mp, param.map_height - mp - param.wall_height):
        for x in range(mp, param.map_height - mp):
          self.bmap[y][x][0] = (tile.blank if random.random()
                                < param.wall_probability else tile.floor)

    def count_wall(x, y):
      cnt = 0
      for dy in range(-1, 2):
        for dx in range(-1, 2):
          if dx == 0 and dy == 0:
            continue
          nx, ny = x + dx, y + dy
          if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
            cnt += 1 if self.bmap[ny][nx][0] == tile.blank else 0
          else:
            cnt += 1
      return cnt

    def simulate():
      for _ in range(param.cellular_iterations):
        new_map = [[tile.blank for _ in range(param.map_width)]
                   for _ in range(param.map_height)]
        for y in range(mp, param.map_height - mp):
          for x in range(mp, param.map_height - mp):
            cnt = count_wall(x, y)
            if self.bmap[y][x][0] == tile.blank:
              new_map[y][
                  x] = tile.blank if cnt >= param.birth_limit else tile.floor
            else:
              new_map[y][
                  x] = tile.blank if cnt > param.death_limit else tile.floor

        for y in range(param.map_height):
          for x in range(param.map_width):
            self.bmap[y][x][0] = new_map[y][x]

    initialize()
    simulate()

  def build_plain(self):
    for y in range(param.map_height):
      for x in range(param.map_width):
        self.bmap[y][x][0] = tile.floor

  def build_perlin_noise(self):
    p = list(range(256))
    random.shuffle(p)
    p = p * 2

    grad3 = [(1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0), (1, 0, 1),
             (-1, 0, 1), (1, 0, -1), (-1, 0, -1), (0, 1, 1), (0, -1, 1),
             (0, 1, -1), (0, -1, -1)]

    def simplex(xin, yin):

      def dot(g, x, y):
        return g[0] * x + g[1] * y

      def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

      def lerp(t, a, b):
        return a + t * (b - a)

      F2 = 0.5 * (math.sqrt(3.0) - 1.0)
      G2 = (3.0 - math.sqrt(3.0)) / 6.0
      s = (xin + yin) * F2
      i = math.floor(xin + s)
      j = math.floor(yin + s)
      t = (i + j) * G2
      X0 = i - t
      Y0 = j - t
      x0 = xin - X0
      y0 = yin - Y0

      if x0 > y0:
        i1, j1 = 1, 0
      else:
        i1, j1 = 0, 1

      x1 = x0 - i1 + G2
      y1 = y0 - j1 + G2
      x2 = x0 - 1.0 + 2.0 * G2
      y2 = y0 - 1.0 + 2.0 * G2

      ii = i & 255
      jj = j & 255
      gi0 = p[ii + p[jj]] % 12
      gi1 = p[ii + i1 + p[jj + j1]] % 12
      gi2 = p[ii + 1 + p[jj + 1]] % 12

      t0 = 0.5 - x0 * x0 - y0 * y0
      if t0 < 0:
        n0 = 0.0
      else:
        t0 *= t0
        n0 = t0 * t0 * dot(grad3[gi0], x0, y0)

      t1 = 0.5 - x1 * x1 - y1 * y1
      if t1 < 0:
        n1 = 0.0
      else:
        t1 *= t1
        n1 = t1 * t1 * dot(grad3[gi1], x1, y1)

      t2 = 0.5 - x2 * x2 - y2 * y2
      if t2 < 0:
        n2 = 0.0
      else:
        t2 *= t2
        n2 = t2 * t2 * dot(grad3[gi2], x2, y2)

      return 70.0 * (n0 + n1 + n2)

    noise = [[
        simplex((x + 2) / param.perlin_scale, (y + 2) / param.perlin_scale)
        for x in range(param.map_width)
    ] for y in range(param.map_height)]

    for y in range(param.map_height):
      for x in range(param.map_width):
        ev = int((noise[y][x] + 1) / 2 * (param.elevation_level + 2))
        self.bmap[y][x][0] = tile.floor_ev[ev]
        self.hmap[y][x] = ev * 2

    for y in range(param.map_height - 1, param.wall_height, -1):
      for x in range(param.map_width):
        if self.bmap[y - param.wall_height - 1][x][0] == self.bmap[y][x][0]:
          for dy in range(param.wall_height):
            self.bmap[y - dy - 1][x][0] = self.bmap[y][x][0]
            self.hmap[y - dy - 1][x] = self.hmap[y][x]

    for y in range(param.map_height - 1):
      for x in range(param.map_width):
        if (self.bmap[y][x][0] > self.bmap[y + 1][x][0]):
          self.make_wall(x, y)

  def make_wall(self, x, y):
    for dy in range(param.wall_height):
      ny = y - dy
      if ny >= 0:
        self.bmap[ny][x][0] = tile.wall
        self.hmap[ny][x] = self.hmap[y + 1][x] + 1

  def place_wall(self):

    def delete_wallcovered_floor():

      def fill_blank(x, y):
        for dy in range(param.wall_height + 1):
          self.bmap[y - dy - 1][x][0] = tile.blank

      for y in range(param.map_height - 1, param.wall_height, -1):
        for x in range(param.map_width):
          if (self.bmap[y - 1][x][0] == tile.blank
              and self.bmap[y][x][0] == tile.floor):
            fill_blank(x, y)

    def fill_hole():
      visited = set()

      def BFS(x, y):
        cnt = 0
        queue = deque([(x, y)])
        catched = set()
        catched.add((x, y))
        visited.add((x, y))
        dire = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
          x, y = queue.popleft()

          for d in dire:
            nx, ny = x + d[0], y + d[1]
            if ny < 0 or ny >= param.map_height or nx < 0 or nx >= param.map_width:
              continue
            if ((nx, ny) not in visited
                and self.bmap[ny][nx][0] == tile.floor):
              visited.add((nx, ny))
              catched.add((nx, ny))
              queue.append((nx, ny))
              cnt += 1

        if cnt <= param.area_threshold:
          for v in catched:
            self.bmap[v[1]][v[0]][0] = tile.blank

      for y in range(param.map_height):
        for x in range(param.map_width):
          if self.bmap[y][x][0] == tile.floor and (x, y) not in visited:
            BFS(x, y)

    delete_wallcovered_floor()
    if param.map_type == 1:
      fill_hole()
    for y in range(param.map_height - 1):
      for x in range(param.map_width):
        if (self.bmap[y][x][0] == tile.blank
            and self.bmap[y + 1][x][0] == tile.floor):
          self.make_wall(x, y)

  def place_ceil(self):
    visited = set()

    def BFS(sx, sy):
      queue = deque([(sx, sy)])
      visited.add((sx, sy))
      dire = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1),
              (-1, 1)]

      while queue:
        x, y = queue.popleft()
        isCeil = False

        for d in dire:
          nx, ny = x + d[0], y + d[1]
          if ny < 0 or ny >= param.map_height or nx < 0 or nx >= param.map_width:
            continue

          nv = self.bmap[ny][nx][0]
          isCeil = isCeil or nv == tile.floor or nv == tile.wall

          if (nx, ny) not in visited and nv == tile.blank:
            visited.add((nx, ny))
            queue.append((nx, ny))

        if isCeil:
          self.bmap[y][x][0] = tile.ceil
          self.hmap[y][x] = 2

    for y in range(param.map_height):
      for x in range(param.map_width):
        if self.bmap[y][x][0] == tile.blank and (x, y) not in visited:
          BFS(x, y)

  def place_structure(self):
    def create_rect_list():
      mg = param.house_margin
      for _ in range(param.house_num):
        strc = param.structure_data[0]
        rects.append(
            (len(strc[0]) + mg[0] + mg[1], len(strc) + mg[2] + mg[3], 0))
      rects.sort(key=lambda x: x[0] * x[1], reverse=True)

    def create_collide_map():
      tm = param.town_boundary_margin
      for y in range(H):
        for x in range(W):
          cmap[y][x] = (0 if tm <= y < H - tm and tm <= x < W - tm
                        and self.bmap[y][x][0] == tile.floor else 1)

    def update_collide_map(x, y, w, h):
      for dy in range(h):
        for dx in range(w):
          cmap[y + dy][x + dx] = 1

    def update_prefix_sum():
      for y in range(H):
        for x in range(W):
          cmap_sum[y][x] = (cmap[y][x] + cmap_sum[y - 1][x] +
                            cmap_sum[y][x - 1] - cmap_sum[y - 1][x - 1])

    def get_area_sum(x1, y1, x2, y2):
      return (cmap_sum[y2][x2] - cmap_sum[y1 - 1][x2] - cmap_sum[y2][x1 - 1] +
              cmap_sum[y1 - 1][x1 - 1])

    rects = []
    create_rect_list()

    H = param.map_height
    W = param.map_width
    cmap = [[0] * (W) for _ in range(H)]
    cmap_sum = [[0] * (W) for _ in range(H)]
    create_collide_map()
    update_prefix_sum()

    def set_structure_position():

      def build_structure_map(x, y, w, h, id):
        strc = param.structure_data[id]
        mg = param.house_margin
        for dy in range(h - mg[2] - mg[3]):
          for dx in range(w - mg[0] - mg[1]):
            self.map[y + dy + mg[2]][x + dx + mg[0]][2] = strc[dy][dx]

      strc_list = []
      for i in range(len(rects)):
        rect = rects[i]
        pos = []
        for y in range(H - rect[1]):
          for x in range(W - rect[0]):
            if get_area_sum(x, y, x + rect[0], y + rect[1]) == 0:
              pos.append((x, y))
        if len(pos) > 0:
          x, y = random.choice(pos)
          build_structure_map(x, y, rect[0], rect[1], rect[2])
          strc_list.append(
              RectArea(x, y, x + rect[0], y + rect[1], len(strc_list)))
          update_collide_map(x, y, rect[0], rect[1])
          update_prefix_sum()
      return strc_list

    def generate_structure_graph(strc_list):
      import heapq

      def prim(start):
        mst = []
        visited = set()
        min_heap = [(0, start, None)]

        while min_heap:
          dist, cur, prev = heapq.heappop(min_heap)
          if cur in visited:
            continue
          visited.add(cur)

          if prev is not None:
            mst.append((prev, cur, dist))

          for next in range(len(rects)):
            new_dist = strc_graph[cur][next]
            if next not in visited:
              heapq.heappush(min_heap, (new_dist, next, cur))

        return mst

      strc_graph = [[0 for _ in range(len(rects))] for _ in range(len(rects))]
      for i in range(len(strc_list)):
        for j in range(len(strc_list)):
          if i != j:
            dist = self.rect_distance(strc_list[i], strc_list[j])
            strc_graph[j][i] = strc_graph[i][j] = dist

      return prim(0)

    def place_path(strc_list, mst):
      W = param.map_width
      H = param.map_height

      def a_star_search(start, end):
        if not (0 <= start[0] < W and 0 <= start[1] < H):
          return
        if not (0 <= end[0] < W and 0 <= end[1] < H):
          return
        if get_area_sum(start[0], start[1], start[0], start[1]) > 0:
          return
        if get_area_sum(end[0], end[1], end[0], end[1]) > 0:
          return

        def heuristic(a, b):
          r = random.uniform(-param.path_random_factor,
                             param.path_random_factor)
          return max(abs(b[0] - a[0]), abs(b[1] - a[1])) + r  # Octile Distance

        def check_corner_pathtile(x, y):
          for i in range(4):
            ok = True
            cdp = [dire[i], dire[(i + 1) % 4], [0, 0]]
            cdp[2][0] = (cdp[0][0]
                         if abs(cdp[0][0]) > abs(cdp[1][0]) else cdp[1][0])
            cdp[2][1] = (cdp[0][1]
                         if abs(cdp[0][1]) > abs(cdp[1][1]) else cdp[1][1])
            for cdpp in cdp:
              nx, ny = x + cdpp[0], y + cdpp[1]
              if not (0 <= nx < W and 0 <= ny < H):
                ok = False
                break
              ok = ok and self.bmap[ny][nx][0] == tile.path
            if ok:
              return True
          return False

        NONE_POS = (-1, -1)
        dist = {(x, y): float('inf') for x in range(W) for y in range(H)}
        dist[start] = 0
        pq = [(0, start)]
        visited = {(x, y): False for x in range(W) for y in range(H)}
        prev = {(x, y): NONE_POS for x in range(W) for y in range(H)}
        dire = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while pq:
          h_dist, (x, y) = heapq.heappop(pq)
          if (x, y) == end:
            break

          if visited[(x, y)]:
            continue
          visited[(x, y)] = True

          for dx, dy in dire:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < W and 0 <= ny < H):
              continue
            if get_area_sum(nx, ny, nx, ny) > 0:
              continue
            if check_corner_pathtile(nx, ny):
              continue

            new_dist = dist[(x, y)] + 1
            if new_dist < dist[(nx, ny)]:
              dist[(nx, ny)] = new_dist
              prev[(nx, ny)] = (x, y)
              heapq.heappush(pq, (new_dist + heuristic(
                  (nx, ny), end), (nx, ny)))

        path = []
        step = end
        while step is not NONE_POS:
          path.append(step)
          step = prev[step]
        path.reverse()

        return path

      def make_path(start, end):
        path = a_star_search(start, end)
        if path is not None:
          for (x, y) in path:
            self.bmap[y][x][0] = tile.path

      for node in mst:
        if node[0] < len(strc_list) and node[1] < len(strc_list):
            A, B = strc_list[node[0]], strc_list[node[1]]
            start_x, start_y = (A.x1 + A.x2) // 2, A.y2
            dest_x, dest_y = (B.x1 + B.x2) // 2, B.y2
            for dy in range(param.house_margin[3]):
              self.bmap[start_y - dy - 1][start_x][0] = tile.path
              self.bmap[dest_y - dy - 1][dest_x][0] = tile.path
            make_path((start_x, start_y), (dest_x, dest_y))

    strc_list = set_structure_position()
    mst = generate_structure_graph(strc_list)
    place_path(strc_list, mst)

  def place_area(self, area_tile, base_id, layer):
    (CAP_MIN, CAP_MAX) = (area_tile.capacity_min, area_tile.capacity_max)
    target = area_tile.id
    prev_tile = {}
    dire = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    class AreaSeed:

      def __init__(self, x, y, direction, magnitude, capacity, base_tile):

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
        self.base = base_tile

    def check_base_id(x, y):
      if param.map_type != 3 or base_id != tile.floor:
        return self.bmap[y][x][0] == base_id
      else:
        return self.bmap[y][x][0] in tile.floor_ev

    def create_seed():
      seed_list = []
      for y in range(param.map_height):
        for x in range(param.map_width):
          if (check_base_id(x, y)
              and random.random() < area_tile.seed_gen_rate):
            seed_list.append(
                AreaSeed(x, y,
                         random.random() * 360, random.random(),
                         random.randint(CAP_MIN, CAP_MAX), self.bmap[y][x][0]))
      return seed_list

    def spread(seed):
      self.bmap[seed.pos[1]][seed.pos[0]][layer] = target
      prev_tile[(seed.pos[0], seed.pos[1])] = seed.base
      buffer = {seed.pos}

      for _ in range(seed.capacity):
        iter_buffer = buffer.copy()
        for v in iter_buffer:
          flag = True
          for i in range(4):
            (x, y) = v[0] + dire[i][0], v[1] + dire[i][1]
            if 0 <= x < param.map_width and 0 <= y < param.map_height:
              flag = flag and self.bmap[y][x][0] != seed.base

          if flag:
            buffer.remove(v)
          else:
            for i in range(4):
              (x, y) = v[0] + dire[i][0], v[1] + dire[i][1]
              if not (0 <= x < param.map_width and 0 <= y < param.map_height):
                continue
              if (self.bmap[y][x][0] == seed.base
                  and random.random() < seed.prob[i]):
                buffer.add((x, y))
                self.bmap[y][x][layer] = target
                prev_tile[(x, y)] = seed.base

    def trim():

      def clean_out(x, y):
        if not (0 <= x < param.map_width and 0 <= y < param.map_height):
          return

        if self.bmap[y][x][layer] == target:
          flag = 0
          for d in dire:
            nx, ny = x + d[0], y + d[1]
            if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
              flag += 1 if self.bmap[ny][nx][layer] != target else 0
          if flag >= 3:
            if layer == 0:
              self.bmap[y][x][layer] = prev_tile[(x, y)]
            else:
              self.bmap[y][x][layer] = 0
            for d in dire:
              clean_out(x + d[0], y + d[1])

      def fill(x, y):
        if check_base_id(x, y):
          flag = True
          for d in dire:
            (nx, ny) = x + d[0], y + d[1]
            if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
              flag = flag and self.bmap[ny][nx][layer] == target

          if flag:
            self.bmap[y][x][layer] = target

      for y in range(param.map_height):
        for x in range(param.map_width):
          clean_out(x, y)

      for y in range(param.map_height):
        for x in range(param.map_width):
          fill(x, y)

    def place_carpet():

      def create_square(x1, y1, x2, y2):
        if x1 < 0 or y1 < 0 or x2 >= param.map_width or y2 >= param.map_height:
          return

        ok = True
        for y in range(y1, y2 + 1):
          for x in range(x1, x2 + 1):
            ok = ok and self.bmap[y][x][0] == base_id
            if layer == 1:
              ok = ok and self.bmap[y][x][layer] == 0

        if ok:
          for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
              self.bmap[y][x][layer] = target

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

        x1, y1 = room.x1, room.y1
        x2, y2 = room.x2 - 1, room.y2 - 1
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
      if param.theme[tx.base.id] != 0:
        self.place_area(tx.base, tile.floor, 0)
    for tx in tile.floor_cover:
      if param.theme[tx.id] != 0:
        self.place_area(tx, tile.floor, 1)
    for tx in tile.extra:
      if param.theme[tx.base.id] != 0:
        for cx in tx.coverList:
          self.place_area(cx, tx.base.id, 1)

  def place_cascade(self, area_tile_set):

    def extend_cascade(px, py):
      x, y = px, py
      while y >= 0 and self.bmap[y][x][0] == tile.wall:
        self.bmap[y][x][0] = cascade_id
        y -= 1

    pd = param.map_padding
    base_id = area_tile_set.base.id
    cascade_id = area_tile_set.cascade.id
    gen_rate = area_tile_set.cascade.seed_gen_rate
    wide_min = area_tile_set.cascade.wide_min
    wide_max = area_tile_set.cascade.wide_max

    for y in range(pd, param.map_height - pd):
      for x in range(pd, param.map_width - pd):
        if (self.bmap[y][x][0] == base_id and y > 0
            and random.random() < gen_rate):
          wide = random.randint(wide_min, wide_max)
          flag = True
          for w in range(wide):
            if x + w < param.map_width:
              flag = (flag and self.bmap[y - 1][x + w][0] == tile.wall
                      and self.bmap[y][x + w][0] == base_id)
            else:
              flag = False
          flag = (flag
                  and (x - 1 == 0 or self.bmap[y - 1][x - 1][0] == tile.wall))
          flag = (flag and (x + wide == param.map_width
                            or self.bmap[y - 1][x + wide][0] == tile.wall))
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
          cond = True
          if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
            cond = (self.bmap[y][x][r] == self.bmap[ny][nx][r]
                    and self.hmap[ny][nx] == self.hmap[y][x])
            if dy == 0:
              cond = (cond
                      or self.bmap[ny][nx][r] in tile.TileCore.type_cascade)
            if self.bmap[y][x][r] in tile.floor_ev:
              if self.bmap[ny][nx][r] == tile.wall:
                cond = cond or self.hmap[ny][nx] == self.hmap[y][x] + 1
              if self.bmap[ny][nx][r] in tile.floor_ev:
                cond = cond or self.hmap[ny][nx] > self.hmap[y][x]
              elif self.bmap[ny][nx][r] in tile.TileCore.type_floor:
                cond = cond or self.hmap[ny][nx] == self.hmap[y][x]
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

      def wallseed_y(tx, ty, target):
        seedy = 1
        while self.bmap[
            ty + seedy][tx][r] == target and ty + seedy < param.map_height:
          seedy += 1
        return ty + seedy

      dmap = [0] * 4
      dire = [(-1, 0), (0, -1), (1, 0), (0, 1)]
      for i in range(4):
        nx, ny = x + dire[i][0], y + dire[i][1]
        cond = True
        if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
          if (self.bmap[ny][nx][r] == tile.wall
              or self.bmap[ny][nx][r] in tile.TileCore.type_cascade):
            nwy = wallseed_y(nx, ny, self.bmap[ny][nx][r])
            wy = wallseed_y(x, y, self.bmap[y][x][r])
            cond = nwy >= wy if dire[i][0] != 0 else True
          else:
            cond = self.hmap[ny][nx] > self.hmap[y][x]

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
        cond = True
        if 0 <= nx < param.map_width:
          cond = self.bmap[y][x][r] == self.bmap[y][nx][r]
        dmap[i] = 1 if cond else 0

      for i in range(len(tile.cascade_automata)):
        automata = tile.cascade_automata[i]
        ok = True
        for j in range(2):
          ok = ok and dmap[j] == automata[j]
        if (ok):
          return i

      return 0

    for y in range(param.map_height):
      for x in range(param.map_width):
        for r in range(2):
          target = self.bmap[y][x][r]
          self.map[y][x][r] = param.theme[target]
          if (target in tile.TileCore.type_floor):
            self.map[y][x][r] += interpolate_floor_tile(x, y, r)
          elif (target in tile.TileCore.type_wall):
            self.map[y][x][r] += interpolate_wall_tile(x, y, r)
          elif (target in tile.TileCore.type_cascade):
            self.map[y][x][r] += interpolate_cascade_tile(x, y, r)

  def place_decorations(self):
    class Prob:
        def __init__(self, target, prob):
          self.target = target
          self.prob = prob

    def convert_to_prob_structure(old_gen):
        new_gen = {
            tile.floor: [],
            tile.wall: [],
        }

        for index, prob_value in enumerate(tile.gen_normal[tile.floor]):
          if prob_value > 0:
            new_gen[tile.floor].append(Prob(target=index, prob=prob_value))
        
        for index, prob_value in enumerate(tile.gen_normal[tile.wall]):
          if prob_value > 0:
            new_gen[tile.wall].append(Prob(target=index, prob=prob_value))

        return new_gen

    gen_deco = convert_to_prob_structure(tile.gen_normal)
    gen_deco_len = {
        tile.floor: len(gen_deco[tile.floor]) + 1,
        tile.wall: len(gen_deco[tile.wall]) + 1,
    }

    def gen_deco_tiles(x, y):
      tiles = []
      tile_basic = self.bmap[y][x][0]
      if param.map_type == 3 and tile_basic in tile.floor_ev:
        tile_basic = tile.floor

      for cond in gen_deco.get(tile_basic, []):
        if (self.map[y][x][tile.layer_data[cond.target]] == tile.transparent
            and random.random() < cond.prob / 10 / gen_deco_len[tile_basic]):
          tiles.append(cond)
      return tiles

    def place_deco(x, y, target):
      group = tile.gen_group.get(target, [])
      ok = True
      for member in group:
        nx, ny = (x + member.dx, y + member.dy)
        if 0 <= nx < param.map_width and 0 <= ny < param.map_height:
          ok = ok and self.map[ny][nx][tile.layer_data[
              member.target]] == tile.transparent
          if member.base_id != -2:
            tile_basic = (self.bmap[y][x][0]
                          if member.base_id == -1 else member.base_id)
            if param.map_type == 3 and tile_basic in tile.floor_ev:
              tile_basic = self.bmap[ny][nx][0]
            ok = ok and self.bmap[ny][nx][0] == tile_basic
        else:
          ok = False

      if ok:
        self.map[y][x][tile.layer_data[target]] = target
        for member in group:
          nx, ny = (x + member.dx, y + member.dy)
          self.map[ny][nx][tile.layer_data[member.target]] = member.target

    for y in range(param.map_height):
      for x in range(param.map_width):
        list = gen_deco_tiles(x, y)
        if len(list) > 0:
          list.sort(key=lambda cond: cond.prob, reverse=True)
          place_deco(x, y, list[0].target)

  def place_shadows(self):
    for y in range(param.map_height):
      for x in range(param.map_width - 1):
        cond1 = self.hmap[y - 1][x] > self.hmap[y][x + 1] if y > 0 else True
        cond2 = self.bmap[y][x + 1][0] in tile.TileCore.type_floor
        cond3 = self.hmap[y][x] > self.hmap[y][x + 1]
        if cond1 and cond2 and cond3:
          self.map[y][x + 1][4] = 5


def main():
  return Dungeon()
