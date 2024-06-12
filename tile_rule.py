class Prob:

    def __init__(self, target, prob):
        self.target = target
        self.prob = prob


class Conf:

    def __init__(self, target, dire):
        self.target = target
        self.dx = dire[0]
        self.dy = dire[1]


blank = '.'
floor = '0'
wall = '1'
ceil = '2'

# Normal Tile Rule
data_prob = {
    floor: {
        (0, 0): [
            Prob('A', 0.005),
            Prob('C', 0.002),
            Prob('D', 0.02),
        ],
    },
    wall: {
        (0, 0): [
            Prob('E', 0.02),
        ],
        (1, 0): [
            Prob('C', 0.02),
        ],
        (-1, 0): [
            Prob('C', 0.02),
        ],
        (0, 1): [
            Prob('C', 0.02),
        ],
        (0, -1): [
            Prob('C', 0.02),
        ],
    },
}

# Group Tile Rule
data_group = {
    'A': [
        Conf('B', (0, 1)),
    ],
}

# Base Tile Rule
data_base = {
    floor: {'A', 'B', 'C', 'D'},
    wall: {'E'},
}
