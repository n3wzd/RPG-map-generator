import tile_rule as tile

# User
tileset_id = 2
map_id = 18

# Dungeon
map_width = 60
map_height = 60
room_min_size = 12
room_max_size = 18
map_padding = 4  # min = 1
room_min_padding = 1
room_max_padding = 1
corridor_wide = 2  # min = 1
wall_height = 3

water_seed_gen_rate = 0.01

theme = {
    tile.blank: 1536,
    tile.floor: 2816,  # 2336
    tile.wall: 7808,  # 4736
    tile.ceil: 7472,  # 6848
    tile.water: 2048,
    tile.cascade: 2480,
}


# Path
class ImagePaths:

  def __init__(self):
    self.A1 = 'resource/Outside_A1.png'
    self.A2 = 'resource/Outside_A2.png'
    self.A3 = 'resource/Outside_A3.png'
    self.A4 = 'resource/Outside_A4.png'
    self.A5 = 'resource/Outside_A5.png'
    self.B = 'resource/Outside_B.png'
    self.C = 'resource/Outside_C.png'


img_path = ImagePaths()

# Constant
TILE_PX_SIZE = 48

# Map Index
# 0 = Base Tile 1
# 1 = Base Tile 2
# 2 = Deco Tile 1
# 3 = Deco Tile 2
# 4 = Shadow Tile
# 5 = Restrict ID (Not Used)
