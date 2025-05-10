
import tkinter as tk
from board import Board


window = Board(tk.Tk(), 400, 13).criar_tabuleiro()
class Stones:
    def __init__(self):
        self.count = 0
        pass

    def click(self):
        self.cor = ["black", "white"][self.count % 2 != 0]
        print("Alguma coisa")
        self.count += 1

    def criar_pedra(self):
        botao = tk.Button(window, text="pedra", command=self.click, fg="orange", font=("Ariel", 20), bg=self.cor)

        botao.pack()
