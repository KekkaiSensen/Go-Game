class GoKnowledge:
    def __init__(self, size):
        self.size = size
        self.center = size // 2

    def get_opening_move(self, stones, move_number):
        # Aumentamos o limite de jogadas de abertura
        if move_number > 12: return None

        # Estratégia de Abertura:
        # 1. Cantos (Hoshi 4-4, Komoku 3-4, Sansan 3-3)
        # 2. Fechamento de Canto (Shimari)
        # 3. Extensão Lateral

        candidates = []

        # Pontos quentes padrão para 19x19 e 13x13
        corners = [
            (3, 3), (self.size - 4, 3),
            (3, self.size - 4), (self.size - 4, self.size - 4),  # Hoshi (4-4)
            (2, 3), (3, 2), (self.size - 3, 3), (self.size - 4, 2)  # Komoku (3-4)
        ]

        if self.size == 9:
            # Em 9x9, o centro e o 3-3 são vitais
            corners = [(4, 4), (2, 2), (6, 2), (2, 6), (6, 6), (2, 4), (4, 2)]

        for r, c in corners:
            if 0 <= r < self.size and 0 <= c < self.size and stones[r][c] == '':
                # Verifica se não tem ninguém colado (para não iniciar luta prematura)
                vizinhos = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if stones[r + dx][c + dy] != '': vizinhos += 1
                if vizinhos == 0:
                    candidates.append((r, c))

        if candidates:
            # Retorna o primeiro disponível
            return candidates[0]

        return None

    def evaluate_shape(self, stones, i, j, color):
        """Avalia a forma local criada pela jogada."""
        score = 0
        opponent = 'white' if color == 'black' else 'black'

        # 1. TRIÂNGULO VAZIO (Bad Shape) - Penalidade
        # (Forma ineficiente que gasta pedras)
        vizinhos_amigos = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if stones[nx][ny] == color: vizinhos_amigos += 1

        if vizinhos_amigos >= 3:
            score -= 15  # Penalidade aumentada

        # 2. HANE (Cabeça de duas/três pedras)
        # Jogar na "quina" do oponente é bom para ataque
        diagonais_inimigas = 0
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                nx, ny = i + dx, j + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if stones[nx][ny] == opponent:
                        diagonais_inimigas += 1

        if diagonais_inimigas > 0:
            score += 5

            # 3. OLHO REAL
        if self.is_real_eye(stones, i, j, color):
            score -= 500  # Não jogue no seu olho

        return score

    def is_real_eye(self, stones, i, j, color):
        """Verifica se (i,j) é um olho verdadeiro do jogador 'color'."""
        # Critério 1: Cruz deve ser amiga/parede
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if stones[nx][ny] != color:
                    return False

        # Critério 2: Diagonais controladas
        enemy_diag = 0
        opponent = 'white' if color == 'black' else 'black'
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                nx, ny = i + dx, j + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if stones[nx][ny] == opponent:
                        enemy_diag += 1

        if enemy_diag >= 2:
            return False

        return True

    def count_liberties(self, stones, i, j):
        libs = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if stones[nx][ny] == '': libs += 1
        return libs