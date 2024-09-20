import numpy as np
from random import shuffle

from tetris.block import block_list

#UIサイズ
WIDTH = 10
HEIGHT = 20
SIZE = 22

#ゲーム
NEXTSIZE = 4

class Board:
    #データ
    data = []

    def __init__(self):
        for x in range(WIDTH):
            self.data.append([])
            for y in range(HEIGHT):
                self.data[x].append(None)

    def is_block_at(self, x, y):
        if(x < 0 or y < 0 or WIDTH <= x or HEIGHT <= y):
            return True

        return not self.data[x][y] == None

class Game:

    #キャンバス
    canvas = None

    #盤面
    board = Board()

    #所持状況
    current = None
    hold = None
    already_hold = False

    #デッキ
    next = []

    def __init__(self, canvas):
        self.canvas = canvas

    def start(self):
        self.take_next()
        self.update()

    def update(self):
        #ミノ処理
        self.current.update()

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

        #盤面の枠を描画
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.canvas.create_rectangle(offX + x * SIZE, offY + y * SIZE, offX + x * SIZE + SIZE, offY + y * SIZE + SIZE, width=1, fill="")
        
        #次のミノを描画
        self.canvas.create_text(offX + WIDTH * SIZE + SIZE / 2 * 3, offY, text="NEXT", anchor="s")
        for i in range(NEXTSIZE):
            block = self.next[i]
            block.paint(offX + WIDTH * SIZE + SIZE / 2 * 3, offY + i * SIZE / 2 * 5 + SIZE / 2 * 2, SIZE / 2, self.canvas)
        
        #現在のミノを表示
        x = (self.current.pos[0] - self.current.center[0]) * SIZE
        y = (self.current.pos[1] - self.current.center[1]) * SIZE
        self.current.paint(offX + x, offY + y, SIZE, self.canvas)


    def take_next(self):
        stock = block_list()
        shuffle(stock)
        for b in stock:
            self.next.append(b)

        self.current = self.next.pop(0)
    
    def hold(self):
        if(self.already_hold):
            return
        
        if(self.hold == None):
            self.hold = self.current
        else:
            temp = self.current
            self.current = self.hold
            self.hold = temp

        self.already_hold = True

    def on_moveleft(self, e):
        self.current.move_left(self.board)

    def on_moveright(self, e):
        self.current.move_right(self.board)
