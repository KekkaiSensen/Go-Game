import random
from heuristics import GoKnowledge


class Bot:
    def __init__(self, size, profundidade_max=2, mode="Médio"):
        self.size = size
        self.profundidade_max = profundidade_max
        self.mode = mode
        self.knowledge = GoKnowledge(size)
        self.memo = {}

    def escolher_jogada(self, stones, cor, history):
        # 1. ABERTURA
        if len(history) < 8 and self.mode in ["Difícil", "Muito Difícil"]:
            opening = self.knowledge.get_opening_move(stones, len(history))
            if opening: return opening

        # 2. INSTINTO
        tactical = self.find_tactical_move(stones, cor, history)
        if tactical: return tactical

        # 3. MINIMAX
        self.memo = {}
        jogadas = self.jogadas_validas_robustas(stones, cor, history)

        if not jogadas: return None

        # Ordenação
        center = self.size // 2

        def sort_key(pos):
            i, j = pos
            score = 0
            if self.captures_opponent(stones, i, j, cor): score += 2000
            dist = abs(i - center) + abs(j - center)
            score -= dist * 10
            if self.mode == "Muito Difícil":
                score += self.knowledge.evaluate_shape(stones, i, j, cor) * 2
            return score

        jogadas.sort(key=sort_key, reverse=True)
        limit = 6 if self.size >= 13 else 10
        jogadas = jogadas[:limit]

        melhor_valor = float('-inf')
        melhor_jogada = None
        alpha = float('-inf')
        beta = float('inf')
        depth = self.profundidade_max
        if len(jogadas) < 8: depth += 1

        for i, j in jogadas:
            novo_tabuleiro = [row[:] for row in stones]
            novo_tabuleiro[i][j] = cor
            valor = self.minimax(novo_tabuleiro, depth - 1, False, cor, alpha, beta)
            valor += random.uniform(0, 0.5)  # Desempate

            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (i, j)
            alpha = max(alpha, melhor_valor)

        return melhor_jogada

    def minimax(self, stones, profundidade, maximizando, cor_jogador, alpha, beta):
        board_hash = self.hash_board(stones, maximizando)
        if board_hash in self.memo:
            cached_depth, cached_val = self.memo[board_hash]
            if cached_depth >= profundidade: return cached_val

        if profundidade == 0:
            score = self.avaliar(stones, cor_jogador)
            self.memo[board_hash] = (profundidade, score)
            return score

        cor_oponente = 'white' if cor_jogador == 'black' else 'black'
        jogador_atual = cor_jogador if maximizando else cor_oponente

        jogadas = self.jogadas_relevantes_locais(stones)
        if not jogadas:
            val = self.avaliar(stones, cor_jogador)
            self.memo[board_hash] = (profundidade, val)
            return val

        if len(jogadas) > 4:
            def quick_sort(pos):
                if self.captures_opponent(stones, pos[0], pos[1], jogador_atual): return 100
                return 0

            jogadas.sort(key=quick_sort, reverse=True)
            jogadas = jogadas[:4]

        if maximizando:
            max_eval = float('-inf')
            for i, j in jogadas:
                novo_tabuleiro = [row[:] for row in stones]
                novo_tabuleiro[i][j] = jogador_atual
                eval_val = self.minimax(novo_tabuleiro, profundidade - 1, False, cor_jogador, alpha, beta)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha: break
            self.memo[board_hash] = (profundidade, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i, j in jogadas:
                novo_tabuleiro = [row[:] for row in stones]
                novo_tabuleiro[i][j] = jogador_atual
                eval_val = self.minimax(novo_tabuleiro, profundidade - 1, True, cor_jogador, alpha, beta)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha: break
            self.memo[board_hash] = (profundidade, min_eval)
            return min_eval

    def avaliar(self, stones, cor_jogador):
        p_jogador, p_oponente = 0, 0
        W_TERRITORIO = 10
        W_LIBERDADE = 2
        W_ATARI = -50
        size = self.size
        for i in range(size):
            for j in range(size):
                pedra = stones[i][j]
                if pedra == '': continue
                libs = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        if stones[nx][ny] == '': libs += 1
                score = W_TERRITORIO + (libs * W_LIBERDADE)
                if libs == 1: score += W_ATARI
                if pedra == cor_jogador:
                    p_jogador += score
                else:
                    p_oponente += score
        return p_jogador - p_oponente

    def find_tactical_move(self, stones, cor, history):
        for i in range(self.size):
            for j in range(self.size):
                if stones[i][j] == '':
                    if self.captures_opponent(stones, i, j, cor):
                        if not self.is_suicide(stones, i, j, cor) and not self.is_ko(stones, i, j, cor, history):
                            return (i, j)
        return None

    def jogadas_validas_robustas(self, stones, cor, history):
        radius = 2 if self.mode == "Muito Difícil" else 1
        candidates = set()
        has_stones = False
        size = self.size
        for i in range(size):
            for j in range(size):
                if stones[i][j] != '':
                    has_stones = True
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            nx, ny = i + dx, j + dy
                            if 0 <= nx < size and 0 <= ny < size and stones[nx][ny] == '':
                                candidates.add((nx, ny))
        validas = []
        lista_analise = list(candidates)
        if not lista_analise and has_stones:
            for i in range(size):
                for j in range(size):
                    if stones[i][j] == '': lista_analise.append((i, j))
        elif not has_stones:
            return [(size // 2, size // 2)]

        for i, j in lista_analise:
            if self.knowledge.is_real_eye(stones, i, j, cor): continue
            if self.is_suicide(stones, i, j, cor): continue
            if self.is_ko(stones, i, j, cor, history): continue
            validas.append((i, j))

        # Fallback global
        if not validas and candidates:
            for i in range(size):
                for j in range(size):
                    if stones[i][j] == '':
                        if (i, j) not in candidates:
                            if not self.is_suicide(stones, i, j, cor) and not self.is_ko(stones, i, j, cor, history):
                                validas.append((i, j))
        return validas

    def jogadas_relevantes_locais(self, stones):
        candidates = set()
        size = self.size
        for i in range(size):
            for j in range(size):
                if stones[i][j] != '':
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < size and 0 <= ny < size and stones[nx][ny] == '':
                            candidates.add((nx, ny))
        return list(candidates)

    def hash_board(self, stones, turn):
        return (tuple(tuple(row) for row in stones), turn)

    def captures_opponent(self, stones, i, j, cor, min_stones=1):
        temp = [row[:] for row in stones]
        temp[i][j] = cor
        oponente = 'white' if cor == 'black' else 'black'
        captura = 0
        for nx, ny in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= nx < self.size and 0 <= ny < self.size and temp[nx][ny] == oponente:
                group = self.get_group_logic(temp, nx, ny)
                if self.is_group_dead_logic(temp, group):
                    captura += len(group)
        return captura >= min_stones

    def is_suicide(self, stones, i, j, cor):
        temp = [row[:] for row in stones]
        temp[i][j] = cor
        if self.captures_opponent(stones, i, j, cor): return False
        group = self.get_group_logic(temp, i, j)
        return self.is_group_dead_logic(temp, group)

    # --- IMPLEMENTAÇÃO DE SUPERKO (Correção Principal) ---
    def is_ko(self, stones, i, j, cor, history):
        if not history: return False

        # Simula o tabuleiro resultante da jogada
        temp = [row[:] for row in stones]
        temp[i][j] = cor
        oponente = 'white' if cor == 'black' else 'black'
        for nx, ny in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= nx < self.size and 0 <= ny < self.size and temp[nx][ny] == oponente:
                group = self.get_group_logic(temp, nx, ny)
                if self.is_group_dead_logic(temp, group):
                    for gx, gy in group: temp[gx][gy] = ''

        # Verifica se esse estado JÁ ACONTECEU em qualquer momento (Superko)
        for state in history:
            if temp == state['stones']:
                return True

        return False

    def get_group_logic(self, board, i, j):
        color = board[i][j];
        group = set();
        stack = [(i, j)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in group: continue
            group.add((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if board[nx][ny] == color: stack.append((nx, ny))
        return group

    def is_group_dead_logic(self, board, group):
        for x, y in group:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if board[nx][ny] == '': return False
        return True