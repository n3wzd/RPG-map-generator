from PIL import Image

import parameter as param

tsz = param.TILE_PX_SIZE
shadow_img = Image.new('RGBA', (24, 24), (0, 0, 0, 127))


def main(map_data, tileset, map_id, output_path):
  map_width, map_height = len(map_data[0]), len(map_data)
  map_img = Image.new('RGBA', (map_width * tsz, map_height * tsz),
                      (0, 0, 0, 0))

  for y in range(len(map_data)):
    for x in range(len(map_data[y])):
      for r in [0, 1, 4, 2, 3]:
        data = map_data[y][x][r]
        if r == 4:
          dt = [(0, 0), (24, 0), (0, 24), (24, 24)]
          for i in range(4):
            if (data >> i) & 1 == 1:
              map_img.paste(shadow_img,
                            (x * tsz + dt[i][0], y * tsz + dt[i][1]),
                            shadow_img)
        else:
          img = tileset[data]
          if img is not None:
            map_img.paste(img, (x * tsz, y * tsz), img)

  filename = f'{output_path}Map{map_id:03}.png'
  map_img.save(filename)
  return filename
