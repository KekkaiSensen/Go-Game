# Go Game

Um jogo de Go implementado em Python utilizando Tkinter e Pygame.

# O que é ?

O Go é um jogo de tabuleiro milenar, criado na China, focado em estratégia e controle territorial. Dois jogadores colocam pedras pretas e brancas buscando cercar áreas e capturar grupos inimigos. Para entender as regras, consulte as [regras do jogo](Regras.md).

## Funcionalidades

- **Modos de Jogo**:
  - Humano vs Bot
  - Humano vs Humano
  - Bot vs Bot (Espectador)
- **Dificuldades do Bot**: Fácil, Médio, Difícil, Muito Difícil.
- **Tamanhos de Tabuleiro**: 9x9, 13x13, 19x19.
- **Regras**: Japonesa (Território) e Chinesa (Área).
- **Efeitos Sonoros**: Sons de pedras e interações.

## Requisitos

- Python 3.x
- Bibliotecas listadas em `requirements.txt`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/KekkaiSensen/Go-Game.git
   cd Go-Game
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como Jogar

Para iniciar o jogo, execute o arquivo `menu.py` localizado na pasta `src` a partir da raiz do projeto:

```bash
python src/menu.py
```

## Estrutura do Projeto

- `src/`: Contém o código fonte do jogo (`game.py`, `menu.py`, `bot.py`, etc).
- `assets/`: Contém recursos gráficos e sonoros.
- `Regras.md`: Explicação detalhada das regras do Go.
