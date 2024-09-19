import numpy as np

WIDTH = 10
HEIGHT = 18
SIZE = 25

class Game:

    #キャンバス
    canvas = None

    #盤面
    board = np.zeros((WIDTH, HEIGHT))

    def __init__(self, canvas):
        self.canvas = canvas

    def start(self):
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
