import tile_rule as tile

# User
tileset_type = ""
tileset_id = 1
map_id = 1

# Map Basic
map_type = 3  # 0: BSP, 1: cellular_automata, 2: plain, 3: perlin_noise
map_width = 64  # min = 10, max = 300
map_height = 64  # min = 10, max = 300
map_padding = 4  # min = 1, max = 9
wall_height = 4  # min = 0, max = 9
deco_rate = 1.0  # min = 0.0, max = 1.0

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
    tile.floor: 7424,
    tile.wall: 7808,
    tile.ceil: 7424,
    tile.path: 2912,
    tile.floor_cover[0].id: 0,
    tile.floor_cover[1].id: 0,
    tile.floor_cover[2].id: 0,
    tile.floor_cover[3].id: 0,
    tile.extra[0].base.id: 0,
    tile.extra[1].base.id: 0,
    tile.extra[2].base.id: 0,
    tile.extra[3].base.id: 0,
}

for f in tile.floor_ev:
    if f not in [tile.floor, tile.ceil]:
        theme[f] = theme[tile.ceil]

structure_data = [
    [
        [0],
    ],
]

# Constant
TILE_PX_SIZE = 48

# Map Layer Index
# 0 = Base Tile 1
# 1 = Base Tile 2
# 2 = Deco Tile 1
# 3 = Deco Tile 2
# 4 = Shadow Tile
# 5 = Restrict ID (Not Used)

# Path
output_path = 'output/'
setting_path = 'settings.ini'
