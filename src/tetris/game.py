from random import shuffle

from tetris.block import block_list

#UIサイズ
WIDTH = 10
HEIGHT = 20
SIZE = 22

#ゲーム
NEXTSIZE = 4

class Board:
    def __init__(self):
        self.data = []
        for x in range(WIDTH):
            self.data.append([])
            for y in range(HEIGHT):
                self.data[x].append(None)

    def is_block_at(self, x, y):
        if(x < 0 or WIDTH <= x or HEIGHT <= y):
            return True

        if(y < 0):
            return False

        return not self.data[x][y] == None
    
    def place_at(self, x, y, color):
        if(x < 0 or y < 0 or WIDTH <= x or HEIGHT <= y):
            return
        
        self.data[x][y] = color

    def check(self):
        line = HEIGHT - 1
        while(line >= 0):
            print(line)
            for i in range(WIDTH):
                if(not self.is_block_at(i, line)):
                    line -= 1
                    break
                elif(i == WIDTH - 1):
                    #ライン消去
                    for j in range(WIDTH):
                        for line2 in range(HEIGHT - line - 1):
                            k = HEIGHT - line2
                            if(k == 0):
                                self.data[j][k] = None
                            else:
                                self.data[j][k] = self.data[j][k - 1]

                    #最初からやり直し
                    line = HEIGHT - 1

    def paint(self, offX, offY, canvas):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = self.data[x][y]
                color = color if not color == None else ""
                canvas.create_rectangle(offX + x * SIZE, offY + y * SIZE, offX + x * SIZE + SIZE, offY + y * SIZE + SIZE, width=1, fill=color)

class Game:

    def __init__(self, canvas):
        self.canvas = canvas
        self.board = Board()
        self.current = None
        self.holding = None
        self.already_hold = False
        self.next = []

    def start(self):
        self.supply()
        self.current = self.take_next()
        self.update()

    def update(self):
        #ミノ処理
        self.current.update(self.board)
        if(self.current.placed):
            self.current = self.take_next()
            self.already_hold = False
            self.board.check()

        #再描画
        self.repaint()

        #次の呼び出し
        self.canvas.after(20, self.update)

    def repaint(self):
        #全クリア
        self.canvas.delete("all")

        #盤面のオフセット
        offX = (self.canvas.winfo_width() - WIDTH * SIZE) / 2
        offY = (self.canvas.winfo_height() - HEIGHT * SIZE) / 2

        #盤面を描画
        self.board.paint(offX, offY, self.canvas)
        
        #次のミノを描画
        self.canvas.create_text(offX + WIDTH * SIZE + SIZE / 2 * 3, offY, text="NEXT", anchor="s")
        for i in range(NEXTSIZE):
            block = self.next[i]
            block.paint(offX + WIDTH * SIZE + SIZE / 2 * 3, offY + i * SIZE / 2 * 5 + SIZE / 2 * 2, SIZE / 2, self.canvas, center = True)

        #ホールド中のミノを表示
        self.canvas.create_text(offX - SIZE / 2 * 4, offY, text="HOLD", anchor="s")
        if(not self.holding == None):
            self.holding.paint(offX - SIZE / 2 * 4, offY + SIZE / 2 * 2, SIZE / 2, self.canvas, center = True)

        #現在のミノを表示
        self.current.paint(offX, offY, SIZE, self.canvas)

    def supply(self):
        stock = block_list()
        shuffle(stock)
        for b in stock:
            self.next.append(b)

    def take_next(self):
        next = self.next.pop(0)
        next.move(3, 0, self.board, absolute = True)

        if(len(self.next) < NEXTSIZE):
            self.supply()

        return next

    def hold(self):
        if(self.already_hold):
            return
        
        if(self.holding == None):
            self.holding = self.take_next()
            self.holding.move(-3, 0, self.board, absolute = True)

        temp = self.current
        self.current = self.holding
        self.current.move(3, 0, self.board, absolute = True)
        self.already_hold = True

        for block in block_list():
            if(block.id == temp.id):
                self.holding = block

    def on_moveleft(self, e):
        self.current.move_left(self.board)

    def on_moveright(self, e):
        self.current.move_right(self.board)
    
    def on_rotate_right(self, e):
        self.current.rotate(90, self.board)

    def on_rotate_left(self, e):
        self.current.rotate(-90, self.board)

    def on_softdrop(self, e):
        self.current.softdrop()
    
    def on_hold(self, e):
        self.hold()
