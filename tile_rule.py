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

    def __init__(self, base, coverList, cascade):
        self.base = base
        self.coverList = coverList
        self.cascade = cascade


class AreaTile:

    def __init__(self, seed_rate=0.002, cap_min=5, cap_max=20):
        self.id = TileCore.id_gen(0)
        self.seed_gen_rate = seed_rate
        self.capacity_min = cap_min
        self.capacity_max = cap_max


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
floor_cover = [AreaTile(0.002), AreaTile(0.002)]
extra = [
    AreaTileSet(
        AreaTile(0.005),
        [AreaTile(0.01, 2, 8), AreaTile(0.01, 2, 8)], CascadeTile())
]


# Normal Deco Tile Rule
class Prob:

    def __init__(self, target, prob):
        self.target = target
        self.prob = prob


gen_normal = {
    floor: [
        Prob(88, 0.01),
        Prob(89, 0.01),
        Prob(90, 0.01),
        Prob(91, 0.01),
        Prob(92, 0.0075),
        Prob(93, 0.0025),
        Prob(95, 0.002),
        Prob(96, 0.005),
        Prob(97, 0.005),
        Prob(98, 0.005),
        Prob(99, 0.005),
        Prob(100, 0.0025),
        Prob(102, 0.0025),
        Prob(103, 0.0025),
    ],
    wall: [
        Prob(192, 0.05),
        Prob(193, 0.05),
    ],
}


# Group Deco Tile Rule
class Group:

    def __init__(self, target, dire):
        self.target = target
        self.dx = dire[0]
        self.dy = dire[1]


gen_group = {
    93: [
        Group(101, (0, 1)),
    ],
    192: [
        Group(200, (0, 1)),
    ],
    193: [
        Group(201, (0, 1)),
    ],
}

# Deco Tile Layer Rule
layer_data = [2] * 9999
layer_data[92:95] = [3] * 4
layer_data[100:103] = [3] * 4

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
