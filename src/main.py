
#インポート
import tkinter as tk
from tetris.game import Game

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

#ウィンドウの作成
window = tk.Tk()

#キャンバスの作成
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

#設定
window.title("Tetris")
window.resizable(False, False)

#ゲームインスタンスを生成
game = Game(canvas)

#イベントを追加
window.bind("<Left>", game.on_moveleft)
window.bind("<Right>", game.on_moveright)
window.bind("<Down>", game.on_softdrop)
window.bind("<Up>", game.on_rotate_right)
window.bind("<KeyPress-z>", game.on_rotate_left)
window.bind("<KeyPress-x>", game.on_hold)
window.bind("<KeyPress-c>", game.on_harddrop)
window.bind("<KeyPress-r>", game.on_reset)

#ゲーム開始
game.start()

#メインループ開始
window.mainloop()
