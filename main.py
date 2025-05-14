import tkinter as tk
from bot import Bot

# Classe GoBoard herda de tk.Tk, que representa a janela principal do jogo
class GoBoard(tk.Tk):

    # Construtor: inicialização do tabuleiro
    def __init__(self, size):
        super().__init__()  # Inicializa a janela Tk
        self.size = size  # Armazena o tamanho do tabuleiro (ex: 13x13)
        self.title("Go Game")  # Define o título da janela

        # Cria um canvas para desenhar o tabuleiro e define a sua cor de fundo
        self.canvas = tk.Canvas(self, width=50*size, height=50*size, bg="orange")
        self.canvas.pack()  # Coloca o canvas na janela
        self.draw_board()  # Chama a função para desenhar o tabuleiro
        self.current_player = 'black'  # Inicializa o jogador atual como 'preto'

        # Associa o clique do botão esquerdo do mouse à função place_stone
        self.canvas.bind("<Button-1>", self.place_stone)

    # Método que desenha o tabuleiro de Go
    def draw_board(self):
        # Inicializa a matriz de pedras vazia (cada posição representa um espaço no tabuleiro)
        self.stones = [['']*self.size for _ in range(self.size)]
        # Desenha as linhas horizontais e verticais do tabuleiro
        for i in range(self.size):
            # Linha horizontal
            self.canvas.create_line(25, 25 + 50 * i, 25 + 50 * (self.size - 1), 25 + 50 * i)
            # Linha vertical
            self.canvas.create_line(25 + 50 * i, 25, 25 + 50 * i, 25 + 50 * (self.size - 1))

    # Método para posicionar uma pedra no tabuleiro
    def place_stone(self, event):
        # Captura as coordenadas do clique do mouse
        x, y = event.x, event.y
        # Converte as coordenadas em índices da grade do tabuleiro
        i = x // 50
        j = y // 50
        # Verifica se a posição está vazia
        if self.stones[i][j] == '':
            # Coloca uma pedra do jogador atual nessa posição
            self.stones[i][j] = self.current_player
            # Desenha a pedra no canvas
            self.draw_stone(i, j, self.current_player)
            # Remove as pedras capturadas após a jogada
            self.remove_captured_stones(i, j)
            # Alterna para o próximo jogador ('preto' -> 'branco' ou 'branco' -> 'preto')
            self.current_player = 'white' if self.current_player == 'black' else 'black'

    # Método que desenha uma pedra no tabuleiro
    def draw_stone(self, i, j, color):
        # Calcula as coordenadas do centro da célula onde a pedra será desenhada
        x = 25 + 50 * i
        y = 25 + 50 * j
        # Desenha um círculo (representando a pedra) no canvas
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, tags=f"stone_{i}_{j}")

    # Método para remover as pedras capturadas
    def remove_captured_stones(self, i, j):
        opponent = 'white' if self.current_player == 'black' else 'black'

        for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if 0 <= x < self.size and 0 <= y < self.size and self.stones[x][y] == opponent:
                grupo = self.get_group(x, y)
                if self.is_group_captured(grupo):
                    for gx, gy in grupo:
                        self.canvas.delete(f"stone_{gx}_{gy}")
                        self.stones[gx][gy] = ''

    
    def get_group(self, i, j):
        color = self.stones[i][j]
        visited = set()
        stack = [(i, j)]

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.stones[nx][ny] == color and (nx, ny) not in visited:
                        stack.append((nx, ny))

        return visited

    
    def is_group_captured(self, group):
        for x, y in group:
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.stones[nx][ny] == '':
                        return False  # Liberdade encontrada
        return True  # Nenhuma liberdade encontrada


    # Método que verifica se um grupo de pedras está cercado (capturado)
    def is_captured(self, i, j):
        stone_color = self.stones[i][j]  # Cor da pedra no grupo que está sendo verificado
        visited = set()  # Conjunto para rastrear as posições já verificadas
        stack = [(i, j)]  # Pilha para realizar a busca (DFS)

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.stones[nx][ny] == '':
                        return False  # O grupo tem liberdade, não está capturado
                    if self.stones[nx][ny] == stone_color and (nx, ny) not in visited:
                        stack.append((nx, ny))

        return True  # Nenhuma liberdade encontrada: grupo capturado

    
    # Método que faz a jogada do bot 
    def bot_move(self):
        i, j = self.bot.escolher_jogada(self.stones, 'white')
        if i is not None and j is not None:
            self.stones[i][j] = 'white'
            self.draw_stone(i, j, 'white')
            self.remove_captured_stones(i, j)
            self.current_player = 'black'


# Função principal do jogo
def main():
    size = 13  # Define o tamanho do tabuleiro
    app = GoBoard(size)  # Cria uma instância do tabuleiro de Go
    app.mainloop()  # Inicia o loop principal da interface gráfica

if __name__ == "__main__":
    main()
