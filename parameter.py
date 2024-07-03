import tile_rule as tile

# User
tileset_id = 2
map_id = 18

# Dungeon
map_width = 100
map_height = 100
room_min_size = 20
room_max_size = 36
map_padding = 4
room_min_padding = 1
room_max_padding = 1
corridor_wide = 2  # min = 1
wall_height = 2

theme = {
    tile.transparent: 0,
    tile.blank: 1536,
    tile.floor: 2816,  # 2336
    tile.wall: 7808,  # 4736
    tile.ceil: 7472,  # 6848
    tile.floor_cover[0].id: 3008,
    tile.floor_cover[1].id: 3920,
    tile.extra[0].base.id: 2048,
    tile.extra[0].coverList[0].id: 2144,
    tile.extra[0].coverList[1].id: 2192,
    tile.extra[0].cascade.id: 2480,
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
