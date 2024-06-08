class Room:

  def __init__(self, x1, y1, x2, y2, id):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.id = id


class Tile:

  def __init__(self, id, init_prob = 0.0, cond=None):
    if cond is None:
      cond = []
    self.id = id
    self.init_prob = init_prob
    self.conditions = cond


class TileCondition:

  def __init__(self, target, direction, prob):
    self.target = target
    self.direction = direction
    self.prob = prob
