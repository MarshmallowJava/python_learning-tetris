
from copy import deepcopy

MAXGRACE = 125
SPEED = 25
class Block:

    pos = [4, 0]
    speed = 0
    grace = 0

    shape = None
    center = None

    color = None

    def __init__(self, shape, center, color):
        self.shape = shape
        self.center = center
        self.color = color
    
    def copy(self):
        return deepcopy(self)
    
    def update(self):
        self.speed += 1
        if(self.speed > SPEED):
            self.pos[1] += 1
            self.speed = 0

    def paint(self, x, y, size, canvas):
        w = len(self.shape)
        h = len(self.shape[0])

        for i in range(w):
            for j in range(h):
                if(self.shape[i][j] == 1):
                    canvas.create_rectangle(x + i * size, y + j * size, x + (i + 1) * size, y + (j + 1) * size, fill = self.color)

    def paint_at(self, x, y, size, canvas):
        w = len(self.shape)
        h = len(self.shape[0])
        width = w * size
        height = h * size
        offX = x - width / 2
        offY = y - height / 2

        self.paint(offX, offY, size, canvas)

S = Block([[0,1],[1,1],[1,0]], (1, 1), "green")
Z = Block([[1,0],[1,1],[0,1]], (1, 1), "red")
L = Block([[0, 1], [0, 1], [1, 1]], (1, 2), "orange")
J = Block([[1, 1],[0, 1],[0, 1]], (1, 2), "blue")
I = Block([[1, 1, 1, 1]], (0, 2), "cyan")
O = Block([[1, 1],[1, 1]], (1, 1), "yellow")
T = Block([[0, 1], [1, 1], [0, 1]], (1, 1), "purple")

def block_list():
    return [S, Z, L, J, I, O, T]
