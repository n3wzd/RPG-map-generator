from PIL import Image

import parameter as param

tsz = param.TILE_PX_SIZE


def main(map, tileset, map_id):
  map_width, map_height = len(map[0]), len(map)
  map_img = Image.new('RGBA', (map_width * tsz, map_height * tsz),
                      (0, 0, 0, 0))

  for y in range(len(map)):
    for x in range(len(map[y])):
      for r in range(len(map[y][x])):
        img = tileset[map[y][x][r]]
        if img is not None:
          map_img.paste(img, (x * tsz, y * tsz), img)

  map_img.save(f'output/Map{map_id:03}.png')
