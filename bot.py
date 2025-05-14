import copy

class Bot:
    def __init__(self, size, profundidade_max=2):
        self.size = size
        self.profundidade_max = profundidade_max

    def escolher_jogada(self, stones, cor):
        melhor_valor = float('-inf')
        melhor_jogada = None

        for i, j in self.jogadas_validas(stones):
            novo_tabuleiro = copy.deepcopy(stones)
            novo_tabuleiro[i][j] = cor
            valor = self.minimax(novo_tabuleiro, self.profundidade_max - 1, False, cor)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (i, j)

        return melhor_jogada

    def minimax(self, stones, profundidade, maximizando, cor_jogador):
        if profundidade == 0:
            return self.avaliar(stones, cor_jogador)

        cor_oponente = 'white' if cor_jogador == 'black' else 'black'
        jogador_atual = cor_jogador if maximizando else cor_oponente

        if maximizando:
            max_eval = float('-inf')
            for i, j in self.jogadas_validas(stones):
                novo_tabuleiro = copy.deepcopy(stones)
                novo_tabuleiro[i][j] = jogador_atual
                aval = self.minimax(novo_tabuleiro, profundidade - 1, False, cor_jogador)
                max_eval = max(max_eval, aval)
            return max_eval
        else:
            min_eval = float('inf')
            for i, j in self.jogadas_validas(stones):
                novo_tabuleiro = copy.deepcopy(stones)
                novo_tabuleiro[i][j] = jogador_atual
                aval = self.minimax(novo_tabuleiro, profundidade - 1, True, cor_jogador)
                min_eval = min(min_eval, aval)
            return min_eval

    def avaliar(self, stones, cor_jogador):
        cor_oponente = 'white' if cor_jogador == 'black' else 'black'
        jogador = sum(row.count(cor_jogador) for row in stones)
        oponente = sum(row.count(cor_oponente) for row in stones)
        return jogador - oponente

    def jogadas_validas(self, stones):
        return [(i, j) for i in range(self.size) for j in range(self.size) if stones[i][j] == '']
