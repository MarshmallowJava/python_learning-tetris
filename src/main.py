
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

#ゲーム開始
game.start()

#メインループ開始
window.mainloop()
