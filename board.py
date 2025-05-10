import tkinter as tk

class Jogador:
    def __init__(self, cor):
        self.cor = cor
        self.coordenadas = []

    def armazena_coordenadas(self, coordenadas):
        self.coordenadas.append(coordenadas)

class Board:
    def __init__(self, root, tamanho, colunas, pedras_instance, jogador_a, jogador_b):
        self.root = root
        self.tamanho = tamanho
        self.colunas = colunas
        self.pedras = pedras_instance
        self.jogador_a = jogador_a
        self.jogador_b = jogador_b
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        self.tabuleiro = tk.Canvas(self.root, width=self.tamanho, height=self.tamanho)
        self.tabuleiro.pack()

        for i in range(self.colunas):
            for j in range(self.colunas):
                x1, y1 = j * (self.tamanho / self.colunas), i * (self.tamanho / self.colunas)
                x2, y2 = x1 + self.tamanho / self.colunas, y1 + self.tamanho / self.colunas
                quadrado_id = self.tabuleiro.create_rectangle(x1, y1, x2, y2, fill="orange")

                # Associar evento de clique a cada quadrado do tabuleiro
                self.tabuleiro.tag_bind(quadrado_id, "<Button-1>", lambda event, linha=i, coluna=j: self.clique_quadrado(linha, coluna))

    def clique_quadrado(self, linha, coluna):
        cor_atual = self.pedras.adicionar_pedra(linha, coluna)
        if cor_atual == "white":
            self.jogador_a.armazena_coordenadas([linha, coluna])
        else:
            self.jogador_b.armazena_coordenadas([linha, coluna])

class Stones:
    def __init__(self, root, tamanho, colunas):
        self.root = root
        self.tamanho = tamanho
        self.count = 0
        self.colunas = colunas
        self.tabuleiro = None  # Referência para o tabuleiro

    def mudar_cor(self):
        self.count += 1
        return "black" if self.count % 2 == 1 else "white"

    def desenhar_pedra(self, coluna, linha):
        x1 = coluna * (self.tamanho / self.colunas)
        y1 = linha * (self.tamanho / self.colunas)
        x2 = x1 + self.tamanho / self.colunas
        y2 = y1 + self.tamanho / self.colunas
        cor = self.mudar_cor()
        self.tabuleiro.create_oval((x1, y1, x2, y2), fill=cor)
        return cor

    def adicionar_pedra(self, linha, coluna):
        return self.desenhar_pedra(coluna, linha)

class Capture:
    def __init__(self):
        pass

    def foi_capturada(self):
        pass

def main():
    tamanho = 500  # Tamanho do tabuleiro em pixels
    colunas = 13   # Quantidade de vezes que serão separados os quadradinhos
    root = tk.Tk()
    root.title("Go")

    jogador_a = Jogador("white")
    jogador_b = Jogador("black")

    pedras = Stones(root, tamanho, colunas)
    tabuleiro = Board(root, tamanho, colunas, pedras, jogador_a, jogador_b)
    pedras.tabuleiro = tabuleiro.tabuleiro  # Passando a referência do tabuleiro para a classe Stones

    root.mainloop()

if __name__ == "__main__":
    main()
