
from copy import deepcopy
class Block:

    shape = None
    center = None

    color = None

    def __init__(self, shape, center, color):
        self.shape = shape
        self.center = center
        self.color = color
    
    def copy(self):
        return deepcopy(self)
    
    def paint(self, x, y, size, canvas):
        w = len(self.shape)
        h = len(self.shape[0])
        width = w * size
        height = h * size
        offx = x - width / 2
        offy = y - height / 2
        
        for i in range(w):
            for j in range(h):
                if(self.shape[i][j] == 1):
                    canvas.create_rectangle(offx + i * size, offy + j * size, offx + (i + 1) * size, offy + (j + 1) * size, fill = self.color)

S = Block([[0,1],[1,1],[1,0]], (1, 1), "green")
Z = Block([[1,0],[1,1],[0,1]], (1, 1), "red")
L = Block([[1, 1, 1],[0, 0, 1]], (1, 2), "orange")
J = Block([[0, 0, 1],[1, 1, 1]], (1, 2), "blue")
I = Block([[1, 1, 1, 1]], (0, 2), "cyan")
O = Block([[1, 1],[1, 1]], (1, 1), "yellow")
T = Block([[0, 1], [1, 1], [0, 1]], (1, 1), "purple")

def block_list():
    return [S, Z, L, J, I, O, T]
