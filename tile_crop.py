from pathlib import Path
from PIL import Image

import parameter as param

tileset = {}
tileset_key = []
tsz = param.TILE_PX_SIZE
tsz2 = tsz // 2
TILESET_LEN = 9999
img_path = {}

def set_img_path():
    def add_path(key, sub_key, value):
      if key not in img_path:
        img_path[key] = {}
        tileset_key.append(key)
        for tk in tk_dt:
          img_path[key][tk] = ""
      img_path[key][sub_key] = value

    folder_path = Path('resource')
    tk_dt = ["A1", "A2", "A3", "A4", "A5", "B", "C", "D", "E"]

    for file in folder_path.rglob('*'):
        if file.is_file():
            for i in range(len(tk_dt)):
                if file.name[-len(tk_dt[i])-5:] == "_" + tk_dt[i] + ".png":
                  add_path(file.name[:-len(tk_dt[i])-5], tk_dt[i], str(file))

set_img_path()

def create_image():
  return Image.new('RGBA', (tsz, tsz), (0, 0, 0, 0))


def open_img(path):
  try:
    return Image.open(path)
  except FileNotFoundError:
    return None
  except PermissionError:
    return None


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


def get_tileset(tile_type):
  A1, A2, A3, A4, A5, B, C, D, E = [[] for _ in range(9)]

  A1_img = open_img(img_path[tile_type]["A1"])
  A2_img = open_img(img_path[tile_type]["A2"])
  A3_img = open_img(img_path[tile_type]["A3"])
  A4_img = open_img(img_path[tile_type]["A4"])
  A5_img = open_img(img_path[tile_type]["A5"])
  B_img = open_img(img_path[tile_type]["B"])
  C_img = open_img(img_path[tile_type]["C"])
  D_img = open_img(img_path[tile_type]["D"])
  E_img = open_img(img_path[tile_type]["E"])

  if (A1_img is not None):
    A1_pre = crop_2D(A1_img, 8, 4, 2 * tsz, 3 * tsz)
    for p in [(0, 0), (0, 1), (3, 0), (3, 1), (4, 0), (7, 0), (4, 1), (7, 1),
              (0, 2), (3, 2), (0, 3), (3, 3), (4, 2), (7, 2), (4, 3), (7, 3)]:
      x, y = p[0], p[1]
      if (x == 7 or (x == 3 and y > 1)):
        A1.append(crop_cascade(A1_pre[y][x]))
      else:
        A1.append(crop_floor(A1_pre[y][x]))

  if (A2_img is not None):
    A2_pre = crop_2D(A2_img, 8, 4, 2 * tsz, 3 * tsz)
    for y in range(4):
      for x in range(8):
        A2.append(crop_floor(A2_pre[y][x]))

  if (A3_img is not None):
    A3_pre = crop_2D(A3_img, 8, 4, 2 * tsz, 2 * tsz)
    for y in range(4):
      for x in range(8):
        A3.append(crop_wall(A3_pre[y][x]))

  if (A4_img is not None):
    A4_pre = crop_A4(A4_img)
    for y in range(6):
      for x in range(8):
        if y % 2 == 0:
          A4.append(crop_floor(A4_pre[y][x]))
        else:
          A4.append(crop_wall(A4_pre[y][x]))

  if (A5_img is not None):
    A5 = crop_1D(A5_img, 8, 16)
  if (B_img is not None):
    B = crop_1D(B_img, 8, 16, 2)
  if (C_img is not None):
    C = crop_1D(C_img, 8, 16, 2)
  if (D_img is not None):
    D = crop_1D(D_img, 8, 16, 2)
  if (E_img is not None):
    E = crop_1D(E_img, 8, 16, 2)

  output = [Image.new('RGBA', (tsz, tsz), (0, 0, 0, 0))] * TILESET_LEN

  def flatten_2d_list(list):
    return [item for row in list for item in row]

  assignments = [
      (2048, 2816, A1, True),
      (2816, 4352, A2, True),
      (4352, 5888, A3, True),
      (5888, 8192, A4, True),
      (1536, 1664, A5, False),
      (0, 256, B, False),
      (256, 512, C, False),
      (512, 768, D, False),
      (768, 1024, E, False),
  ]
  for (start, end, data, flatten) in assignments:
    if data:
      output[start:end] = flatten_2d_list(data) if flatten else data

  return output

def main():
  for key in tileset_key:
    tileset[key] = get_tileset(key)
  return tileset
