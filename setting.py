import configparser
import os
import parameter as param
import tile_rule as tile

def save_ini():
    config = configparser.ConfigParser()

    config.add_section('General')
    config.set('General', 'tileset_type', param.tileset_type)
    config.set('General', 'tileset_id', str(param.tileset_id))
    config.set('General', 'map_id', str(param.map_id))

    config.add_section('MapBasic')
    config.set('MapBasic', 'map_width', str(param.map_width))
    config.set('MapBasic', 'map_height', str(param.map_height))
    config.set('MapBasic', 'map_padding', str(param.map_padding))
    config.set('MapBasic', 'map_type', str(param.map_type))
    config.set('MapBasic', 'wall_height', str(param.wall_height))
    config.set('MapBasic', 'deco_rate', str(param.deco_rate))

    config.add_section('Dungeon')
    config.set('Dungeon', 'room_min_size', str(param.room_min_size))
    config.set('Dungeon', 'room_max_size', str(param.room_max_size))
    config.set('Dungeon', 'room_padding', str(param.room_padding))
    config.set('Dungeon', 'corridor_wide_auto', str(param.corridor_wide_auto))
    config.set('Dungeon', 'corridor_wide', str(param.corridor_wide))
    config.set('Dungeon', 'room_freq', str(param.room_freq))

    config.add_section('Cave')
    config.set('Cave', 'wall_probability', str(param.wall_probability))
    config.set('Cave', 'cellular_iterations', str(param.cellular_iterations))

    config.add_section('Structure')
    config.set('Structure', 'path_random_factor', str(param.path_random_factor))
    config.set('Structure', 'house_num', str(param.house_num))
    config.set('Structure', 'town_boundary_margin', str(param.town_boundary_margin))

    config.add_section('Field')
    config.set('Field', 'perlin_scale', str(param.perlin_scale))
    config.set('Field', 'elevation_level', str(param.elevation_level))

    config.add_section('Tile')
    config.set('Tile', 'transparent', str(param.theme[tile.transparent]))
    config.set('Tile', 'blank', str(param.theme[tile.blank]))
    config.set('Tile', 'floor', str(param.theme[tile.floor]))
    config.set('Tile', 'wall', str(param.theme[tile.wall]))
    config.set('Tile', 'ceil', str(param.theme[tile.ceil]))
    config.set('Tile', 'path', str(param.theme[tile.path]))
    config.set('Tile', 'vertex', str(param.theme[tile.vertex]))
    config.set('Tile', 'floor_cover_0', str(param.theme[tile.floor_cover[0].id]))
    config.set('Tile', 'floor_cover_1', str(param.theme[tile.floor_cover[1].id]))
    config.set('Tile', 'floor_cover_2', str(param.theme[tile.floor_cover[2].id]))
    config.set('Tile', 'floor_cover_3', str(param.theme[tile.floor_cover[3].id]))
    config.set('Tile', 'extra_0', str(param.theme[tile.extra[0].base.id]))
    config.set('Tile', 'extra_1', str(param.theme[tile.extra[1].base.id]))
    config.set('Tile', 'extra_2', str(param.theme[tile.extra[2].base.id]))
    config.set('Tile', 'extra_3', str(param.theme[tile.extra[3].base.id]))

    with open(param.setting_path, 'w') as configfile:
        config.write(configfile)

def load_ini():
    if not os.path.exists(param.setting_path):
        return
    
    config = configparser.ConfigParser()
    config.read(param.setting_path)

    param.tileset_type = config.get('General', 'tileset_type')
    param.tileset_id = config.getint('General', 'tileset_id')
    param.map_id = config.getint('General', 'map_id')

    param.map_width = config.getint('MapBasic', 'map_width')
    param.map_height = config.getint('MapBasic', 'map_height')
    param.map_padding = config.getint('MapBasic', 'map_padding')
    param.map_type = config.getint('MapBasic', 'map_type')
    param.wall_height = config.getint('MapBasic', 'wall_height')
    param.deco_rate = config.getint('MapBasic', 'deco_rate')

    param.room_min_size = config.getint('Dungeon', 'room_min_size')
    param.room_max_size = config.getint('Dungeon', 'room_max_size')
    param.room_padding = config.getint('Dungeon', 'room_padding')
    param.corridor_wide = config.getint('Dungeon', 'corridor_wide')
    param.room_freq = config.getint('Dungeon', 'room_freq')

    param.wall_probability = config.getint('Cave', 'wall_probability')
    param.cellular_iterations = config.getint('Cave', 'cellular_iterations')

    param.path_random_factor = config.getint('Structure', 'path_random_factor')
    param.house_num = config.getint('Structure', 'house_num')
    param.town_boundary_margin = config.getint('Structure', 'town_boundary_margin')

    param.perlin_scale = config.getint('Field', 'perlin_scale')
    param.elevation_level = config.getint('Field', 'elevation_level')

    param.theme[tile.transparent] = config.getint('Tile', 'transparent')
    param.theme[tile.blank] = config.getint('Tile', 'blank')
    param.theme[tile.floor] = config.getint('Tile', 'floor')
    param.theme[tile.wall] = config.getint('Tile', 'wall')
    param.theme[tile.ceil] = config.getint('Tile', 'ceil')
    param.theme[tile.path] = config.getint('Tile', 'path')
    param.theme[tile.vertex] = config.getint('Tile', 'vertex')
    param.theme[tile.floor_cover[0].id] = config.getint('Tile', 'floor_cover_0')
    param.theme[tile.floor_cover[1].id] = config.getint('Tile', 'floor_cover_1')
    param.theme[tile.floor_cover[2].id] = config.getint('Tile', 'floor_cover_2')
    param.theme[tile.floor_cover[3].id] = config.getint('Tile', 'floor_cover_3')
    param.theme[tile.extra[0].base.id] = config.getint('Tile', 'extra_0')
    param.theme[tile.extra[1].base.id] = config.getint('Tile', 'extra_1')
    param.theme[tile.extra[2].base.id] = config.getint('Tile', 'extra_2')
    param.theme[tile.extra[3].base.id] = config.getint('Tile', 'extra_3')
