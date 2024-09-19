
class Block:

    shape = None
    center = None

    def __init__(self, shape, center):
        self.shape = shape
        self.center = center

S = Block([[0,1],[1,1],[1,0]], (1, 1))
Z = Block([[1,0],[1,1],[0,1]], (1, 1))
L = Block([[1, 1, 1],[0, 0, 1]], (1, 2))
J = Block([[0, 0, 1],[1, 1, 1]], (1, 2))
I = Block([[1, 1, 1, 1]], (0, 2))
O = Block([[1, 1],[1, 1]], (1, 1))
T = Block([0, 1], [1, 1], [0, 1], (1, 1))

def block_list():
    return [S, Z, L, Z, I, O, T]
