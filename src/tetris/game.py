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
        count = 0

        line = HEIGHT - 1
        while(line >= 0):
            for i in range(WIDTH):
                if(not self.is_block_at(i, line)):
                    line -= 1
                    break
                elif(i == WIDTH - 1):
                    count += 1
                    #ライン消去
                    for j in range(WIDTH):
                        for line2 in range(line + 1):
                            k = line - line2
                            if(k == 0):
                                self.data[j][k] = None
                            else:
                                self.data[j][k] = self.data[j][k - 1]

                    #最初からやり直し
                    line = HEIGHT - 1
    
        return count

    def paint(self, offX, offY, canvas):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                color = self.data[x][y]
                color = color if not color == None else ""
                canvas.create_rectangle(offX + x * SIZE, offY + y * SIZE, offX + x * SIZE + SIZE, offY + y * SIZE + SIZE, width=1, fill=color)
    
    def nothing_there(self):
        for line in self.data:
            for b in line:
                if(not b == None):
                    return False
        
        return True

class Game:

    def __init__(self, canvas):
        self.canvas = canvas

        #ボード情報
        self.board = Board()

        #操作中のミノ
        self.current = None

        #ホールド
        self.holding = None
        self.already_hold = False

        #デッキ
        self.next = []

        #連数
        self.ren = -1

        #T-Spin
        self.t_spin = 0

        #パフェ達成
        self.perfect = False

        #消去アニメーション
        self.anim_delay = 0

    def start(self):
        self.supply()
        self.update()

    def update(self):
        if(self.anim_delay == 0):
            #所持ミノがなければ供給
            if(self.current == None):
                self.current = self.take_next()

            #ミノ処理
            self.current.update(self.board)

            #設置されたなら判定
            if(self.current.placed):
                count = self.board.check()
                if(count > 0):
                    self.anim_delay = 25
                    self.ren += 1

                    self.t_spin = count
                    if(not self.current.t_spin):
                        self.t_spin = 0

                    if(self.board.nothing_there()):
                        self.perfect = True
                    else:
                        self.perfect = False
                else:
                    self.ren = -1

                self.current = None
                self.already_hold = False                
        else:
            self.anim_delay -= 1

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

        #REN数
        if(self.ren > 0):
            self.canvas.create_text(10, offY, text=str(self.ren) + "REN", anchor="sw")
        
        if(self.t_spin > 0 and self.anim_delay > 0):
            label = ["T-Spin Mini", "T-Spin Double", "T-Spin Triple"]
            self.canvas.create_text(10, offY + 20, text=label[self.t_spin - 1], anchor="sw")

        if(self.perfect and self.anim_delay > 0):
            self.canvas.create_text(10, offY + 40, text="PERFECT CLEAR", anchor="sw")

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
        if(not self.current == None):
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
        if(not self.current == None):
            self.current.move_left(self.board)

    def on_moveright(self, e):
        if(not self.current == None):
            self.current.move_right(self.board)
    
    def on_rotate_right(self, e):
        if(not self.current == None):
            self.current.rotate(90, self.board)

    def on_rotate_left(self, e):
        if(not self.current == None):
            self.current.rotate(-90, self.board)

    def on_softdrop(self, e):
        if(not self.current == None):
            self.current.softdrop()
    
    def on_harddrop(self, e):
        if(not self.current == None):
            self.current.harddrop()
    
    def on_hold(self, e):
        if(not self.current == None):
            self.hold()

    def on_reset(self, e):
        self.__init__(self.canvas)
        self.supply()