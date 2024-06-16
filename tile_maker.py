from PIL import Image
import tile_rule as tile

tileset = []
tsz = tile.tile_size
tsz2 = tsz // 2


def create_image():
  return Image.new('RGBA', (tsz, tsz), (0, 0, 0, 0))


def crop_2D(img, W, H, width=tsz, height=tsz):
  output = [[None for _ in range(W)] for _ in range(H)]
  for y in range(H):
    for x in range(W):
      region = (x * width, y * height, (x + 1) * width, (y + 1) * height)
      output[y][x] = img.crop(region)
  return output


def crop_A4(img, W=8, H=6, width=2 * tsz):
  output = [[None for _ in range(W)] for _ in range(H)]
  h = 0
  for y in range(H):
    height = tsz * (3 if y % 2 == 0 else 2)
    for x in range(W):
      region = (x * width, h, (x + 1) * width, h + height)
      output[y][x] = img.crop(region)
    h += height
  return output


def crop_1D(img, W, H, P=1, width=tsz, height=tsz):
  output = []
  for p in range(P):
    for y in range(H):
      for x in range(W):
        region = (p * W * tsz + x * width, y * height,
                  p * W * tsz + (x + 1) * width, (y + 1) * height)
        output.append(img.crop(region))
  return output


def crop_floor(img):

  def paste(id, a, b, c, d):
    output[id].paste(data[a[1]][a[0]], (0, 0))
    output[id].paste(data[b[1]][b[0]], (tsz2, 0))
    output[id].paste(data[c[1]][c[0]], (0, tsz2))
    output[id].paste(data[d[1]][d[0]], (tsz2, tsz2))

  output = [create_image() for _ in range(48)]
  data = crop_2D(img, 4, 6, tsz2, tsz2)
  for i in range(16):
    a = (2, 0) if (i >> 0) & 1 else (2, 4)
    b = (3, 0) if (i >> 1) & 1 else (1, 4)
    c = (2, 1) if (i >> 3) & 1 else (2, 3)
    d = (3, 1) if (i >> 2) & 1 else (1, 3)
    paste(i, a, b, c, d)

  for i in range(4):
    b = (3, 0) if (i >> 0) & 1 else (1, 4)
    d = (3, 1) if (i >> 1) & 1 else (1, 3)
    paste(16 + i, (0, 4), b, (0, 3), d)

  for i in range(4):
    c = (2, 1) if (i >> 1) & 1 else (2, 3)
    d = (3, 1) if (i >> 0) & 1 else (1, 3)
    paste(20 + i, (2, 2), (1, 2), c, d)

  for i in range(4):
    a = (2, 0) if (i >> 1) & 1 else (2, 4)
    c = (2, 1) if (i >> 0) & 1 else (2, 3)
    paste(24 + i, a, (3, 4), c, (3, 3))

  for i in range(4):
    a = (2, 0) if (i >> 0) & 1 else (2, 4)
    b = (3, 0) if (i >> 1) & 1 else (1, 4)
    paste(28 + i, a, b, (2, 5), (1, 5))

  paste(32, (0, 4), (3, 4), (0, 3), (3, 3))
  paste(33, (2, 2), (1, 2), (2, 5), (1, 5))

  paste(34, (0, 2), (1, 2), (0, 3), (1, 3))
  paste(35, (0, 2), (1, 2), (0, 3), (3, 1))
  paste(36, (2, 2), (3, 2), (2, 3), (3, 3))
  paste(37, (2, 2), (3, 2), (2, 1), (3, 3))
  paste(38, (2, 4), (3, 4), (2, 5), (3, 5))
  paste(39, (2, 0), (3, 4), (2, 5), (3, 5))
  paste(40, (0, 4), (1, 4), (0, 5), (1, 5))
  paste(41, (0, 4), (3, 0), (0, 5), (1, 5))

  paste(42, (0, 2), (3, 2), (0, 3), (3, 3))
  paste(43, (0, 2), (1, 2), (0, 5), (1, 5))
  paste(44, (0, 4), (3, 4), (0, 5), (3, 5))
  paste(45, (2, 2), (3, 2), (2, 5), (3, 5))

  paste(46, (0, 2), (3, 2), (0, 5), (3, 5))
  paste(47, (0, 0), (1, 0), (0, 1), (1, 1))

  return output


def crop_cascade(img):

  def paste(id, a, b, c, d):
    output[id].paste(data[a[1]][a[0]], (0, 0))
    output[id].paste(data[b[1]][b[0]], (tsz2, 0))
    output[id].paste(data[c[1]][c[0]], (0, tsz2))
    output[id].paste(data[d[1]][d[0]], (tsz2, tsz2))

  output = [create_image() for _ in range(48)]
  data = crop_2D(img, 4, 6, tsz2, tsz2)
  paste(0, (2, 0), (1, 0), (2, 1), (2, 1))
  paste(1, (0, 0), (1, 0), (0, 1), (1, 1))
  paste(2, (2, 0), (3, 0), (2, 1), (3, 1))
  paste(3, (0, 0), (3, 0), (0, 1), (3, 1))

  return output


def crop_wall(img):

  def paste(id, a, b, c, d):
    output[id].paste(data[a[1]][a[0]], (0, 0))
    output[id].paste(data[b[1]][b[0]], (tsz2, 0))
    output[id].paste(data[c[1]][c[0]], (0, tsz2))
    output[id].paste(data[d[1]][d[0]], (tsz2, tsz2))

  output = [create_image() for _ in range(48)]
  data = crop_2D(img, 4, 4, tsz2, tsz2)
  paste(0, (2, 1), (1, 1), (2, 2), (1, 2))
  paste(1, (0, 1), (1, 1), (0, 2), (1, 2))
  paste(2, (2, 0), (1, 0), (2, 1), (1, 1))
  paste(3, (0, 0), (1, 0), (0, 1), (1, 1))
  paste(4, (2, 1), (3, 1), (2, 2), (3, 2))
  paste(5, (0, 1), (3, 1), (0, 2), (3, 2))
  paste(6, (2, 0), (3, 0), (2, 1), (3, 1))
  paste(7, (0, 0), (3, 0), (0, 1), (3, 1))

  paste(8, (2, 2), (1, 2), (2, 3), (1, 3))
  paste(9, (0, 2), (1, 2), (0, 3), (1, 3))
  paste(10, (2, 0), (1, 0), (2, 3), (1, 3))
  paste(11, (0, 0), (1, 0), (0, 3), (1, 3))
  paste(12, (2, 2), (3, 2), (2, 3), (3, 3))
  paste(13, (0, 2), (3, 2), (0, 3), (3, 3))
  paste(14, (2, 0), (3, 0), (2, 3), (3, 3))
  paste(15, (0, 0), (3, 0), (0, 3), (3, 3))

  return output


def main():
  A1 = []
  A1_pre = crop_2D(Image.open('resource/Outside_A1.png'), 8, 4, 2 * tsz,
                   3 * tsz)
  for y in range(4):
    for x in range(8):
      if (x == 1 or x == 2 or x == 5 or x == 6):
        continue
      if (x == 7 or (x == 3 and y > 1)):
        A1.append(crop_cascade(A1_pre[y][x]))
      else:
        A1.append(crop_floor(A1_pre[y][x]))

  A2 = []
  A2_pre = crop_2D(Image.open('resource/Outside_A2.png'), 8, 4, 2 * tsz,
                   3 * tsz)
  for y in range(4):
    for x in range(8):
      A2.append(crop_floor(A2_pre[y][x]))

  A3 = []
  A3_pre = crop_2D(Image.open('resource/Outside_A3.png'), 8, 4, 2 * tsz,
                   2 * tsz)
  for y in range(4):
    for x in range(8):
      A3.append(crop_wall(A3_pre[y][x]))

  A4 = []
  A4_pre = crop_A4(Image.open('resource/Outside_A4.png'))
  for y in range(4):
    for x in range(8):
      if y % 2 == 0:
        A4.append(crop_floor(A4_pre[y][x]))
      else:
        A4.append(crop_wall(A4_pre[y][x]))

  A5 = crop_1D(Image.open('resource/Outside_A5.png'), 8, 16)
  B = crop_1D(Image.open('resource/Outside_B.png'), 8, 16, 2)
  C = crop_1D(Image.open('resource/Outside_C.png'), 8, 16, 2)

  print2(B)


def print2(output):
  test = Image.new('RGBA', (tsz * 8, tsz * 32), (0, 0, 0, 0))
  for y in range(32):
    for x in range(8):
      test.paste(output[y * 8 + x], (x * tsz, y * tsz))
  test.save('output.png')
