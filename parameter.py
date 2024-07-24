import tile_rule as tile

# User
tileset_id = 2
map_id = 18

# Map Basic
map_width = 64
map_height = 64
map_padding = 4
map_type = 2  # 0: BSP, 1: cellular_automata, 2: plain

## Dungeon(BSP)
room_min_size = 4  # only floor
room_max_size = 20  # only floor
room_min_padding = 1
room_max_padding = 2
corridor_wide_auto = False
corridor_wide = 1
wall_height = 2
room_freq = 0.75

## Cave(cellular_automata)
wall_probability = 0.50
cellular_iterations = 4
birth_limit = 4
death_limit = 4
area_threshold = 20

## Town(A*)
path_random_factor = 3
house_num = 5
house_min_margin = 5
town_boundary_margin = 8

# Theme
theme = {
    tile.transparent: 0,
    tile.blank: 1536,
    tile.floor: 2816,
    tile.wall: 7184,  # 7808
    tile.ceil: 6800,  # 7472
    # tile.extra[0].base.id: 2912,  # 2048
    tile.path: 2912,
    tile.house: 2144,
}

# tile.floor_cover[0].id: 3008,  # 3008
# tile.floor_cover[1].id: 3488,  # 3920
# tile.extra[0].coverList[0].id: 2144,
# tile.extra[0].coverList[1].id: 2192,
# tile.extra[0].cascade.id: 2480,


# Path
class ImagePaths:

  def __init__(self):
    self.A1 = 'resource/Inside_A1.png'
    self.A2 = 'resource/Inside_A2.png'
    self.A3 = 'resource/Inside_A3.png'
    self.A4 = 'resource/Inside_A4.png'
    self.A5 = 'resource/Inside_A5.png'
    self.B = 'resource/Inside_B.png'
    self.C = 'resource/Inside_C.png'
    self.D = 'resource/Inside_D.png'
    self.E = 'resource/Inside_E.png'


img_path = ImagePaths()

# Constant
TILE_PX_SIZE = 48

# Map Layer Index
# 0 = Base Tile 1
# 1 = Base Tile 2
# 2 = Deco Tile 1
# 3 = Deco Tile 2
# 4 = Shadow Tile
# 5 = Restrict ID (Not Used)
