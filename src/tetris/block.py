
MAXGRACE = 25
SPEED = 25

class Tetrimino:

    def __init__(self, shape, center, color):
        self.center = center
        self.speed = 0
        self.grace = 0
        self.drop = False
        self.placed = False

        self.blocks = []
        for x in range(len(shape)):
            for y in range(len(shape[x])):
                if(shape[x][y] == 1):
                    block = Block([x, y], color)
                    self.blocks.append(block)

    def update(self, board):
        if(self.is_ground(board)):
            self.grace += 1
            if(self.grace > MAXGRACE or (self.drop and self.grace > MAXGRACE / 2)):
                self.place(board)
        else:
            self.speed += 1
            if(self.speed > SPEED):
                self.move(0, 1, board)
                self.speed = 0

        self.drop = False

    def move_left(self, board):
        self.move(-1, 0, board)

    def move_right(self, board):
        self.move(1, 0, board)
    
    def move(self, dx, dy, board):
        if(self.is_collide(dx, dy, board)):
            return

        for block in self.blocks:
            block.move(dx, dy)

        self.center[0] += dx
        self.center[1] += dy

    def rotate(self, angle, board):

        for block in self.blocks:
            if(not block.can_rotate(angle, self.center[0], self.center[1], board)):
                return
        
        for block in self.blocks:
            block.rotate(angle, self.center[0], self.center[1])

    def softdrop(self):
        self.speed = SPEED
        self.drop = True
    
    def place(self, board):
        for block in self.blocks:
            block.place(board)
        self.placed = True

    def is_collide(self, dx, dy, board):
        for block in self.blocks:
            if(block.is_collide(dx, dy, board)):
                return True
        
        return False

    def is_ground(self, board):
        if(self.is_collide(0, 1, board)):
            return True

        return False

    def is_collide(self, x, y, board):
        for block in self.blocks:
            if(block.is_collide(x, y, board)):
                return True
        return False
    
    def paint(self, x, y, size, canvas, center = False):
        if(center):
            width = self.width() * size
            height = self.height() * size
            x -= width / 2
            y -= height / 2

        for block in self.blocks:
            block.paint(x, y, size, canvas)

    def width(self):
        return self.len(0)

    def height(self):
        return self.len(1)

    def len(self, index):
        min = self.blocks[0].pos[index]
        max = self.blocks[0].pos[index]

        for block in self.blocks:
            if(block.pos[index] < min):
                min = block.pos[index]
            if(block.pos[index] > max):
                max = block.pos[index]

        return max - min

class Block:

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def place(self, board):
        board.place_at(self.pos[0], self.pos[1], self.color)

    def is_collide(self, dx, dy, board):
        return board.is_block_at(self.pos[0] + dx, self.pos[1] + dy)
    
    def can_rotate(self, r, cx, cy, board):
        s = Block.sin(r)
        c = Block.cos(r)

        nx = (self.pos[0] - cx) * c - (self.pos[1] - cy) * s + cx
        ny = (self.pos[0] - cx) * s + (self.pos[1] - cy) * c + cy

        return not board.is_block_at(nx, ny)
    
    def rotate(self, r, cx, cy):
        s = Block.sin(r)
        c = Block.cos(r)

        nx = int((self.pos[0] - cx) * c - (self.pos[1] - cy) * s + cx)
        ny = int((self.pos[0] - cx) * s + (self.pos[1] - cy) * c + cy)

        self.pos[0] = nx
        self.pos[1] = ny

    def paint(self, x, y, size, canvas):
        canvas.create_rectangle(x + self.pos[0] * size, y + self.pos[1] * size, x + (self.pos[0] + 1) * size, y + (self.pos[1] + 1) * size, fill=self.color)
    
    def sin(angle):
        if(angle == 90):
            return 1
        elif(angle == -90):
            return -1
        else:
            return 0

    def cos(angle):
        if(angle == 90):
            return 0
        elif(angle == -90):
            return 0
        else:
            return 1

def block_list():
    S = Tetrimino([[0,1],[1,1],[1,0]], [1.5, 1], "green")
    Z = Tetrimino([[1,0],[1,1],[0,1]], [1.5, 1], "red")
    L = Tetrimino([[0, 1], [0, 1], [1, 1]], [1, 1.5], "orange")
    J = Tetrimino([[1, 1],[0, 1],[0, 1]], [1, 1.5], "blue")
    I = Tetrimino([[1, 1, 1, 1]], [0, 2], "cyan")
    O = Tetrimino([[1, 1],[1, 1]], [0.5, 0.5], "yellow")
    T = Tetrimino([[0, 1], [1, 1], [0, 1]], [1, 1], "purple")
    return [S, Z, L, J, I, O, T]
