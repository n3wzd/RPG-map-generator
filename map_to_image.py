from PIL import Image
import tile_rule as tile

tile_size = 104  # px

data = {
    tile.floor: Image.open('resource/floor.png'),
    tile.wall: Image.open('resource/wall.png'),
    tile.ceil: Image.open('resource/ceil.png'),
}


def process(map):
  map_width, map_height = len(map[0]), len(map)
  map_img = Image.new('RGB', (map_width * tile_size, map_height * tile_size))

  for y in range(len(map)):
    for x in range(len(map[y])):
      img = data.get(map[y][x])
      if img is not None:
        map_img.paste(img, (x * tile_size, y * tile_size))

  map_img.save('dungeon.jpg')
