
from copy import deepcopy

MAXGRACE = 50
SPEED = 25

class Block:
    def __init__(self, shape, center, color):
        self.shape = shape
        self.center = center
        self.color = color
        self.pos = [4, 2]
        self.speed = 0
        self.grace = 0
        self.placed = False

    def move_left(self, board):
        if(not self.is_collide(self.pos[0] - 1, self.pos[1], board)):
            self.pos[0] += -1

    def move_right(self, board):
        if(not self.is_collide(self.pos[0] + 1, self.pos[1], board)):
            self.pos[0] += 1

    def is_ground(self, board):
        return self.is_collide(self.pos[0], self.pos[1] + 1, board)

    def is_collide(self, x, y, board):
        w = len(self.shape)
        h = len(self.shape[0])

        for bx in range(w):
            for by in range(h):
                block = self.shape[bx][by]
                wx = x - self.center[0] + bx
                wy = y - self.center[1] + by

                if(block == 1 and board.is_block_at(wx, wy) == 1):
                    return True
        
        return False
    
    def place_at(self, board):
        self.placed = True

        w = len(self.shape)
        h = len(self.shape[0])

        for bx in range(w):
            for by in range(h):
                block = self.shape[bx][by]
                wx = self.pos[0] - self.center[0] + bx
                wy = self.pos[1] - self.center[1] + by
                if(block == 1):
                    board.place_at(wx, wy, self.color)

    def copy(self):
        return deepcopy(self)
    
    def update(self, board):
        if(self.is_ground(board)):
            self.grace += 1
            if(self.grace > MAXGRACE):
                self.place_at(board)
        else:
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
