from math import floor

MAXGRACE = 25
SPEED = 25

#右回転
SRSDATA0 = [
    [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
]
#左回転
SRSDATA1 = [
    [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],          #0   -> #270
    [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],         #90  -> 0
    [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],       #180 -> 90
    [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]       #270 -> 180
]

class Tetrimino:

    def __init__(self, shape, center, color, color2):
        self.id = color
        self.shadow = color2
        self.shadow_depth = -1
        self.center = center
        self.speed = 0
        self.grace = 0
        self.placed = False
        self.angle = 0
        self.reset_count = 8

        self.blocks = []
        for x in range(len(shape)):
            for y in range(len(shape[x])):
                if(shape[x][y] == 1):
                    block = Block([x, y], color)
                    self.blocks.append(block)

    def update(self, board):
        if(self.is_ground(board)):
            self.grace += 1
            if(self.grace > MAXGRACE):
                self.place(board)
        else:
            self.speed += 1
            if(self.speed > SPEED):
                self.move(0, 1, board)
                self.speed = 0
        
        i = 0
        while(True):
            if(self.is_collide(0, i + 1, board)):
                break
            i += 1
        self.shadow_depth = i

    def move_left(self, board):
        if(self.move(-1, 0, board)):
            if(self.grace > 0):
                self.reset_grace()        

    def move_right(self, board):
        if(self.move(1, 0, board)):
            if(self.grace > 0):
                self.reset_grace()
    
    def move(self, dx, dy, board, absolute = False):
        if(not absolute and self.is_collide(dx, dy, board)):
            return False

        for block in self.blocks:
            block.move(dx, dy)

        self.center[0] += dx
        self.center[1] += dy

        return True

    def rotate(self, angle, board):
        index = self.angle
        index = (index + 360 if index < 0 else index) % 360
        index = int(index / 90)

        srsdata = SRSDATA0[index] if angle > 0 else SRSDATA1[index]

        for d in srsdata:
            flag = True

            for block in self.blocks:
                if(not block.can_rotate(d[0], d[1], angle, self.center[0], self.center[1], board)):
                    flag = False
                    break


            if(flag):
                self.angle += angle
                self.angle = (self.angle + 360 if self.angle < 0 else self.angle) % 360

                for block in self.blocks:
                    block.rotate(d[0], d[1], angle, self.center[0], self.center[1])
                
                self.center[0] += d[0]
                self.center[1] += d[1]

                if(self.grace > 0):
                    self.reset_grace()

                return

    def softdrop(self):
        self.speed = SPEED
    
    def harddrop(self):
        self.move(0, self.shadow_depth, None, absolute=True)
        self.grace = MAXGRACE
    
    def reset_grace(self):
        if(self.reset_count > 0):
            self.grace = 0
            self.reset_count -= 1
    
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

        if(not self.shadow_depth == -1):
            for block in self.blocks:
                block.paint(x, y + self.shadow_depth * size, size, canvas, color = self.shadow)

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
    
    def can_rotate(self, dx, dy, r, cx, cy, board):
        s = Block.sin(r)
        c = Block.cos(r)

        x = self.pos[0]
        y = self.pos[1]
        nx = Block.cast((x - cx) * c - (y - cy) * s + cx) + dx
        ny = Block.cast((x - cx) * s + (y - cy) * c + cy) + dy

        return not board.is_block_at(nx, ny)

    def rotate(self, dx, dy, r, cx, cy):
        s = Block.sin(r)
        c = Block.cos(r)

        x = self.pos[0]
        y = self.pos[1]
        nx = Block.cast((x - cx) * c - (y - cy) * s + cx) + dx
        ny = Block.cast((x - cx) * s + (y - cy) * c + cy) + dy

        self.pos[0] = nx
        self.pos[1] = ny

    def paint(self, x, y, size, canvas, color = None):
        color = self.color if color == None else color
        canvas.create_rectangle(x + self.pos[0] * size, y + self.pos[1] * size, x + (self.pos[0] + 1) * size, y + (self.pos[1] + 1) * size, fill=color)
    
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

    def cast(f):
        return floor(f) if f < 0 else int(f)

def block_list():
    S = Tetrimino([[0,1],[1,1],[1,0]], [1, 1], "#00ee00", "#88ff88")
    Z = Tetrimino([[1,0],[1,1],[0,1]], [1, 1], "#ee0000", "#ff8888")
    L = Tetrimino([[0, 1], [0, 1], [1, 1]], [1, 1], "#ffaa00", "#ffdd99")
    J = Tetrimino([[1, 1],[0, 1],[0, 1]], [1, 1], "#0000ee", "#8888ff")
    I = Tetrimino([[1], [1], [1], [1]], [2, 0.5], "#00e8e8", "#88fcfc")
    O = Tetrimino([[1, 1],[1, 1]], [0.5, 0.5], "#eeee00", "#ffff88")
    T = Tetrimino([[0, 1], [1, 1], [0, 1]], [1, 1], "#aa22ee", "#dd88ff")
    return [S, Z, L, J, I, O, T]
