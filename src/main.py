
#インポート
import tkinter as tk
from tetris.game import Game

#ウィンドウの作成
window = tk.Tk()

#キャンバスの作成
canvas = tk.Canvas(window, width=640, height=480)
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
