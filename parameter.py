import tile_rule as tile

# User
tileset_type = ""
tileset_id = 1
map_id = 1

# Map Basic
map_type = 0
map_width = 64
map_height = 64
map_padding = 4
wall_height = 4
deco_rate = 80

## Dungeon(BSP)
room_min_size = 4
room_max_size = 20
room_padding = 0
corridor_wide_auto = True
corridor_wide = 2
room_freq = 75

## Cave(cellular_automata)
wall_probability = 50
cellular_iterations = 4
birth_limit = 4
death_limit = 4
area_threshold = 20

## Town(A*, MST)
path_random_factor = 3
house_num = 0
house_margin = (1, 1, 1, 0)  # (left, right, up, bottom), min = 0, max = 9
town_boundary_margin = 3  # min = 0, max = 9

## Field(perlin_noise)
perlin_scale = 100
elevation_level = 1

## Boundary
map_type_dispaly = ["Dungeon", "Cave", "Plain", "Field"]
map_type_map = dict(zip(map_type_dispaly, [0, 1, 2, 3]))

boundary = {
    "tileset_id": lambda: (0, 9999),
    "map_id": lambda: (0, 9999),
    "map_width": lambda: (20, 300),
    "map_height": lambda: (20, 300),
    "map_padding": lambda: (0, 9),
    "wall_height": lambda: (1, 9),
    "deco_rate": lambda: (0, 100),
    "house_num": lambda: (0, 15),
    "room_min_size": lambda: (4, max(4, (min(map_width, map_height) - map_padding) // 4)),
    "room_max_size": lambda: (4, max(4, (min(map_width, map_height) - map_padding) // 4)),
    "room_padding": lambda: (0, room_min_size // 2),
    "corridor_wide": lambda: (1, (room_min_size - wall_height) // 2),
    "room_freq": lambda: (0, 100),
    "path_random_factor": lambda: (0, 5),
    "wall_probability": lambda: (40, 60),
    "cellular_iterations": lambda: (1, 10),
    "perlin_scale": lambda: (50, 200),
    "elevation_level": lambda: (0, 3),
}

# Theme
theme = {
    tile.transparent: 0,
    tile.blank: 1536,
    tile.floor: 7424,
    tile.wall: 7808,
    tile.ceil: 7424,
    tile.path: 2912,
    tile.vertex: 1,
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

tilegen_normal = {
    tile.floor: [0] * 1024,
    tile.wall: [0] * 1024,
}

# Constant
TILE_PX_SIZE = 48
output_path = 'output/'
setting_path = 'settings.ini'
