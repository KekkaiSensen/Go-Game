class GoKnowledge:
    def __init__(self, size):
        self.size = size
        self.center = size // 2

    def get_opening_move(self, stones, move_number):
        if move_number > 8: return None

        # Estratégia de Abertura: Cantos e Lados
        # Prioridade: 4-4 (Hoshi) -> 3-4 (Komoku)
        candidates = [
            (3, 3), (self.size - 4, 3),
            (3, self.size - 4), (self.size - 4, self.size - 4),
            (2, 3), (3, 2), (self.size - 3, 3), (self.size - 4, 2)
        ]

        for r, c in candidates:
            if 0 <= r < self.size and 0 <= c < self.size and stones[r][c] == '':
                # Se canto está vazio, joga nele
                return (r, c)
        return None

    def evaluate_shape(self, stones, i, j, color):
        """Avalia a forma local criada pela jogada."""
        score = 0
        opponent = 'white' if color == 'black' else 'black'

        # 1. TRIÂNGULO VAZIO (Bad Shape) - Penalidade
        vizinhos_amigos = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if stones[nx][ny] == color: vizinhos_amigos += 1

        # Se formar um bloco aglomerado, penaliza levemente
        if vizinhos_amigos >= 3:
            score -= 10

        # 2. HANE (Cabeça de pedra)
        # Se jogar diagonal a uma pedra inimiga que está em contato com amiga
        # (Detecção simplificada: Se tem inimigo adjacente)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and stones[nx][ny] == opponent:
                score += 5  # Luta/Contato

        # 3. OLHO REAL (Evitar preencher seu próprio olho)
        if self.is_real_eye(stones, i, j, color):
            score -= 500  # JAMAIS jogue dentro do seu próprio olho verdadeiro

        return score

    def is_real_eye(self, stones, i, j, color):
        """Verifica se (i,j) é um olho verdadeiro do jogador 'color'."""
        # Critério 1: Todos vizinhos diretos (cruz) devem ser amigos ou borda
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if stones[nx][ny] != color:
                    return False  # Tem buraco ou inimigo

        # Critério 2: Diagonais controladas (simplificado)
        # Se tiver inimigos nas diagonais, pode ser olho falso.
        enemy_diag = 0
        total_diag = 0
        opponent = 'white' if color == 'black' else 'black'
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                nx, ny = i + dx, j + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    total_diag += 1
                    if stones[nx][ny] == opponent:
                        enemy_diag += 1

        # Regra simplificada: Se mais de 1 diagonal for inimiga, é olho falso
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