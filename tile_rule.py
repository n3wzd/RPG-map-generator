# Basic Tile ID List
class TileCore:
    id_cnt = -1
    type_floor = set()
    type_wall = set()
    type_cascade = set()

    @staticmethod
    def id_gen(type=-1):
        TileCore.id_cnt += 1
        if type == 0:
            TileCore.type_floor.add(TileCore.id_cnt)
        if type == 1:
            TileCore.type_wall.add(TileCore.id_cnt)
        if type == 2:
            TileCore.type_cascade.add(TileCore.id_cnt)
        return TileCore.id_cnt


class AreaTileSet:

    def __init__(self, base, coverList=None, cascade=None):
        self.base = base
        self.coverList = coverList if coverList is not None else []
        self.cascade = cascade


class AreaTile:

    def __init__(self, seed_rate=0.002, cap_min=5, cap_max=20, carpet=False):
        self.id = TileCore.id_gen(0)
        self.seed_gen_rate = seed_rate
        self.capacity_min = cap_min
        self.capacity_max = cap_max
        self.carpet = carpet  # only BSP


class CascadeTile:

    def __init__(self, seed_rate=0.1, wide_min=2, wide_max=3):
        self.id = TileCore.id_gen(2)
        self.seed_gen_rate = seed_rate
        self.wide_min = wide_min
        self.wide_max = wide_max


transparent = TileCore.id_gen()
blank = TileCore.id_gen()
floor = TileCore.id_gen(0)
wall = TileCore.id_gen(1)
ceil = TileCore.id_gen(0)
floor_cover = [
    AreaTile(seed_rate=0.002, cap_min=10, cap_max=15),
    AreaTile(seed_rate=0.002, cap_min=10, cap_max=15),
    AreaTile(seed_rate=0.002, cap_min=10, cap_max=15),
    AreaTile(seed_rate=0.002, cap_min=10, cap_max=15),
]
extra = [
    AreaTileSet(AreaTile(seed_rate=0.002, cap_min=10, cap_max=15)),
    AreaTileSet(AreaTile(seed_rate=0.002, cap_min=10, cap_max=15)),
    AreaTileSet(AreaTile(seed_rate=0.002, cap_min=10, cap_max=15)),
    AreaTileSet(AreaTile(seed_rate=0.002, cap_min=10, cap_max=15)),
]
path = TileCore.id_gen(0)
vertex = TileCore.id_gen()
floor_ev = [floor, ceil] + [TileCore.id_gen(0)] * 4

# Group Deco Tile Rule
class Group:

    def __init__(self, target, dire, base_id=-1):
        self.target = target
        self.dx = dire[0]
        self.dy = dire[1]
        self.base_id = base_id  # -1: same with origin, -2: don't care


gen_group = {}

# Deco Tile Layer Rule
layer_data = [2] * 9999

# Tile Automata
floor_automata = [
    [[1, 1, 1], [1, 2, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 2, 1], [1, 1, 1]],
    [[1, 1, 0], [1, 2, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 2, 1], [1, 1, 1]],
    [[1, 1, 1], [1, 2, 1], [1, 1, 0]],
    [[0, 1, 1], [1, 2, 1], [1, 1, 0]],
    [[1, 1, 0], [1, 2, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 2, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 2, 1], [0, 1, 1]],
    [[0, 1, 1], [1, 2, 1], [0, 1, 1]],
    [[1, 1, 0], [1, 2, 1], [0, 1, 1]],
    [[0, 1, 0], [1, 2, 1], [0, 1, 1]],
    [[1, 1, 1], [1, 2, 1], [0, 1, 0]],
    [[0, 1, 1], [1, 2, 1], [0, 1, 0]],
    [[1, 1, 0], [1, 2, 1], [0, 1, 0]],
    [[0, 1, 0], [1, 2, 1], [0, 1, 0]],
    [[2, 1, 1], [0, 2, 1], [2, 1, 1]],
    [[2, 1, 0], [0, 2, 1], [2, 1, 1]],
    [[2, 1, 1], [0, 2, 1], [2, 1, 0]],
    [[2, 1, 0], [0, 2, 1], [2, 1, 0]],
    [[2, 0, 2], [1, 2, 1], [1, 1, 1]],
    [[2, 0, 2], [1, 2, 1], [1, 1, 0]],
    [[2, 0, 2], [1, 2, 1], [0, 1, 1]],
    [[2, 0, 2], [1, 2, 1], [0, 1, 0]],
    [[1, 1, 2], [1, 2, 0], [1, 1, 2]],
    [[1, 1, 2], [1, 2, 0], [0, 1, 2]],
    [[0, 1, 2], [1, 2, 0], [1, 1, 2]],
    [[0, 1, 2], [1, 2, 0], [0, 1, 2]],
    [[1, 1, 1], [1, 2, 1], [2, 0, 2]],
    [[0, 1, 1], [1, 2, 1], [2, 0, 2]],
    [[1, 1, 0], [1, 2, 1], [2, 0, 2]],
    [[0, 1, 0], [1, 2, 1], [2, 0, 2]],
    [[2, 1, 2], [0, 2, 0], [2, 1, 2]],
    [[2, 0, 2], [1, 2, 1], [2, 0, 2]],
    [[2, 0, 2], [0, 2, 1], [2, 1, 1]],
    [[2, 0, 2], [0, 2, 1], [2, 1, 0]],
    [[2, 0, 2], [1, 2, 0], [1, 1, 2]],
    [[2, 0, 2], [1, 2, 0], [0, 1, 2]],
    [[1, 1, 2], [1, 2, 0], [2, 0, 2]],
    [[0, 1, 2], [1, 2, 0], [2, 0, 2]],
    [[2, 1, 1], [0, 2, 1], [2, 0, 2]],
    [[2, 1, 0], [0, 2, 1], [2, 0, 2]],
    [[2, 0, 2], [0, 2, 0], [2, 1, 2]],
    [[2, 0, 2], [0, 2, 1], [2, 0, 2]],
    [[2, 1, 2], [0, 2, 0], [2, 0, 2]],
    [[2, 0, 2], [1, 2, 0], [2, 0, 2]],
    [[2, 0, 2], [0, 2, 0], [2, 0, 2]],
    [[2, 0, 2], [0, 2, 0], [2, 0, 2]],
]

wall_automata = []
for i in range(16):
    wall_automata.append([
        (i >> 0) & 1 ^ 1,  # left
        (i >> 1) & 1 ^ 1,  # up
        (i >> 2) & 1 ^ 1,  # right
        (i >> 3) & 1 ^ 1,  # down
    ])

cascade_automata = []
for i in range(4):
    cascade_automata.append([
        (i >> 0) & 1 ^ 1,  # left
        (i >> 1) & 1 ^ 1,  # right
    ])
