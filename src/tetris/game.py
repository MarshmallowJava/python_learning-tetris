import numpy as np
from random import shuffle

from tetris.block import block_list

#UIサイズ
WIDTH = 10
HEIGHT = 18
SIZE = 25

#ゲーム
NEXTSIZE = 4

class Game:

    #キャンバス
    canvas = None

    #盤面
    board = np.zeros((WIDTH, HEIGHT))
    current = None

    #デッキ
    next = []

    def __init__(self, canvas):
        self.canvas = canvas

    def start(self):
        self.take_next()
        self.update()

    def update(self):

        #再描画
        self.repaint()

        #次の呼び出し
        self.canvas.after(20, self.update)

    def repaint(self):
        self.canvas.delete("all")

        offX = (self.canvas.winfo_width() - WIDTH * SIZE) / 2
        offY = (self.canvas.winfo_height() - HEIGHT * SIZE) / 2

        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.canvas.create_rectangle(offX + x * SIZE, offY + y * SIZE, offX + x * SIZE + SIZE, offY + y * SIZE + SIZE, width=1, fill="")
        
        for i in range(NEXTSIZE):
            block = self.next[i]
            block.paint(offX + WIDTH * SIZE + SIZE / 2 * 3, offY + i * SIZE / 2 * 5 + SIZE / 2 * 2, SIZE / 2, self.canvas)

    def take_next(self):
        stock = block_list()
        shuffle(stock)
        for b in stock:
            self.next.append(b)

        self.current = self.next.pop(0)
