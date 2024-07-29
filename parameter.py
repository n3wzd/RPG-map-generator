import tile_rule as tile

# User
tileset_id = 1
map_id = 18

# Map Basic
map_width = 64  # min = 10, max = 300
map_height = 64  # min = 10, max = 300
map_padding = 4  # min = 1, max = 9
map_type = 3  # 0: BSP, 1: cellular_automata, 2: plain, 3: perlin_noise
wall_height = 4  # min = 0, max = 9

## Dungeon(BSP)
room_min_size = 4  # min = 4, max = min(w, h) - pd, only floor
room_max_size = 20
room_padding = 1  # min = 0, max = rmsz // 2
corridor_wide_auto = False
corridor_wide = 1  # min = 1, max = (rmsz - wh) // 2
room_freq = 0.75  # min = 0.0, max = 1.0

## Cave(cellular_automata)
wall_probability = 0.50  # min = 0.4, max = 0.6
cellular_iterations = 4  # min = 1, max = 10
birth_limit = 4
death_limit = 4
area_threshold = 20

## Town(A*, MST)
path_random_factor = 3  # min = 0, max = 5
house_num = 0  # min = 0, max = 15
house_margin = (1, 1, 1, 0)  # (left, right, up, bottom), min = 0, max = 9
town_boundary_margin = 3  # min = 0, max = 9

## Field(perlin_noise)
perlin_scale = 100  # min = 50, max = 200
elevation_level = 1  # min = 0, max = 3

# Theme
theme = {
    tile.transparent: 0,
    tile.blank: 1536,
    tile.floor: 7424,  # 2816
    tile.wall: 7808,  # 7184
    tile.ceil: 7424,  # 6800
    tile.extra[0].base.id: 2048,  # 2912
    tile.path: 2912,
}

for f in tile.floor_ev:
    if f not in [tile.floor, tile.ceil]:
        theme[f] = theme[tile.ceil]

# tile.floor_cover[0].id: 3008,  # 3008
# tile.floor_cover[1].id: 3488,  # 3920
# tile.extra[0].coverList[0].id: 2144,
# tile.extra[0].coverList[1].id: 2192,
# tile.extra[0].cascade.id: 2480,

structure_data = [
    [
        [208, 209, 210],
        [216, 217, 218],
        [224, 225, 226],
    ],
    [
        [232, 233, 234],
        [240, 241, 242],
        [248, 249, 250],
    ],
]


# Path
class ImagePaths:

    def __init__(self, id):
        if id == 1:
            self.A1 = 'resource/Outside_A1.png'
            self.A2 = 'resource/Outside_A2.png'
            self.A3 = 'resource/Outside_A3.png'
            self.A4 = 'resource/Outside_A4.png'
            self.A5 = 'resource/Outside_A5.png'
            self.B = 'resource/Outside_B.png'
            self.C = 'resource/Outside_C.png'
            self.D = 'resource/Outside_D.png'
            self.E = 'resource/Outside_E.png'
        if id == 2:
            self.A1 = 'resource/Inside_A1.png'
            self.A2 = 'resource/Inside_A2.png'
            self.A3 = 'resource/Inside_A3.png'
            self.A4 = 'resource/Inside_A4.png'
            self.A5 = 'resource/Inside_A5.png'
            self.B = 'resource/Inside_B.png'
            self.C = 'resource/Inside_C.png'
            self.D = 'resource/Inside_D.png'
            self.E = 'resource/Inside_E.png'


img_path = ImagePaths(tileset_id)

# Constant
TILE_PX_SIZE = 48

# Map Layer Index
# 0 = Base Tile 1
# 1 = Base Tile 2
# 2 = Deco Tile 1
# 3 = Deco Tile 2
# 4 = Shadow Tile
# 5 = Restrict ID (Not Used)
