from PIL import Image

import tile_rule as tile

tsz = tile.tile_size


def main(map, tileset):
  map_width, map_height = len(map[0]), len(map)
  map_img = Image.new('RGB', (map_width * tsz, map_height * tsz))

  for y in range(len(map)):
    for x in range(len(map[y])):
      img = tileset[map[y][x][0]]
      if img is not None:
        map_img.paste(img, (x * tsz, y * tsz))

  map_img.save('dungeon.jpg')
