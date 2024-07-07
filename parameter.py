import tile_rule as tile

# User
tileset_id = 2
map_id = 18

# Dungeon
map_width = 30
map_height = 30
room_min_size = 8
room_max_size = 12
map_padding = 4  # min = 1
room_min_padding = 0
room_max_padding = 0
corridor_wide_auto = True
corridor_wide = 2  # min = 1
wall_height = 2

theme = {
    tile.transparent: 0,
    tile.blank: 1536,
    tile.floor: 2816,
    tile.wall: 7184,  # 7808
    tile.ceil: 6800,  # 7472
    tile.extra[0].base.id: 2912,  # 2048
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
