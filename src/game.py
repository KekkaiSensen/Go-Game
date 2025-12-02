import tkinter as tk
from tkinter import messagebox
import threading
import pygame  # Substituindo winsound por pygame para suportar arquivos de mídia
import os
from bot import Bot


class GoBoard(tk.Tk):
    def __init__(self, size=13, difficulty='Médio', player_color='black',
                 rules='Japonesa', game_mode='HvB', sound_enabled=True):
        super().__init__()
        self.size = size
        self.player_color = player_color
        self.rules = rules
        self.game_mode = game_mode
        self.sound_enabled = sound_enabled

        # --- Inicializar Audio (Pygame) ---
        pygame.mixer.init()
        self.sounds = {}
        # --- Inicializar Audio (Pygame) ---
        pygame.mixer.init()
        self.sounds = {}
        try:
            # Carregando os sons da pasta assets
            # IMPORTANTE: Certifique-se de que os arquivos na pasta são .wav

            # Som da pedra
            if os.path.exists("assets/audio/stone_sound.wav"):
                self.sounds["move"] = pygame.mixer.Sound("assets/audio/stone_sound.wav")
            else:
                print("Aviso: 'assets/audio/stone_sound.wav' não encontrado.")

            # Som do bot (start)
            if os.path.exists("assets/audio/bot_start.wav"):
                self.sounds["bot_start"] = pygame.mixer.Sound("assets/audio/bot_start.wav")
            else:
                print("Aviso: 'assets/audio/bot_start.wav' não encontrado.")

        except Exception as e:
            print(f"Erro ao carregar sons: {e}")

        # --- Configuração de Título ---
        mode_str = ""
        if game_mode == 'HvH':
            mode_str = "(Pessoa vs Pessoa)"
        elif game_mode == 'BvB':
            mode_str = "(Bot vs Bot)"
        else:
            mode_str = "(Pessoa vs Bot)"
        self.title(f"Go ({size}x{size}) - {difficulty} - {rules} {mode_str}")

        # --- Variáveis de Estado ---
        self.last_move = None
        self.scoring_mode = False
        self.dead_stones = set()
        self.ghost_stone = None
        self.total_moves = 0
        self.max_moves = (size * size) * 3
        self.is_thinking = False

        # --- Ajuste Dinâmico de Tamanho ---
        if self.size == 19:
            self.cell_size = 30;
            self.offset = 30
        elif self.size == 13:
            self.cell_size = 40;
            self.offset = 40
        else:
            self.cell_size = 50;
            self.offset = 45

        # --- Layout Principal ---
        self.main_frame = tk.Frame(self, bg="#2C3E50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Carregamento de Assets (Imagem) ---
        self.board_image = None
        try:
            if os.path.exists("assets/madeira.png"):
                self.original_image = tk.PhotoImage(file="assets/madeira.png")
                self.board_image = self.original_image
            elif os.path.exists("madeira.png"):  # Tenta na raiz também
                self.original_image = tk.PhotoImage(file="madeira.png")
                self.board_image = self.original_image
        except:
            self.board_image = None

        board_bg_color = "#E0B968"
        canvas_width = self.cell_size * self.size + (self.offset * 2)
        canvas_height = self.cell_size * self.size + (self.offset * 2)

        self.canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height,
                                bg=board_bg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)

        if self.board_image:
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.board_image)

        # --- Painel Lateral ---
        self.side_panel = tk.Frame(self.main_frame, padx=20, bg="#ECF0F1", width=220)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.side_panel.pack_propagate(False)

        self.label_turn = tk.Label(self.side_panel, text="Vez: Preto", font=("Helvetica", 16, "bold"), bg="#ECF0F1")
        self.label_turn.pack(pady=20)

        self.captures = {'black': 0, 'white': 0}
        self.komi = 6.5

        self.score_label = tk.Label(self.side_panel, text=self.get_score_text(), font=("Consolas", 11),
                                    justify=tk.LEFT, bg="#BDC3C7", padx=10, pady=10, relief="sunken")
        self.score_label.pack(pady=10, fill=tk.X)

        self.status_label = tk.Label(self.side_panel, text="", font=("Arial", 10, "bold"),
                                     bg="#ECF0F1", fg="#C0392B", wraplength=180)
        self.status_label.pack(pady=5)

        # --- Botões ---
        btn_style = {"font": ("Arial", 11, "bold"), "height": 2, "relief": tk.FLAT}

        self.pass_btn = tk.Button(self.side_panel, text="Passar Vez", command=self.human_pass,
                                  bg="#E74C3C", fg="white", **btn_style)
        self.pass_btn.pack(pady=5, fill=tk.X)

        self.undo_btn = tk.Button(self.side_panel, text="Desfazer", command=self.undo_move,
                                  bg="#95A5A6", fg="white", **btn_style)
        self.undo_btn.pack(pady=5, fill=tk.X)

        self.hint_btn = tk.Button(self.side_panel, text="💡 Dica", command=self.give_hint,
                                  bg="#F1C40F", fg="black", **btn_style)
        self.hint_btn.pack(pady=5, fill=tk.X)

        if self.game_mode == 'BvB': self.hint_btn.pack_forget()

        self.finish_btn = tk.Button(self.side_panel, text="Confirmar Fim", command=self.calculate_final_score,
                                    bg="#27AE60", fg="white", **btn_style)

        # --- Inicialização ---
        self.draw_board_grid()

        depth_map = {'Fácil': 1, 'Médio': 2, 'Difícil': 3, 'Muito Difícil': 4}
        bot_depth = depth_map.get(difficulty, 2)
        if size == 9 and difficulty == 'Muito Difícil': bot_depth = 6

        self.current_player = 'black'
        self.stones = [[''] * self.size for _ in range(self.size)]
        self.bot = Bot(size, profundidade_max=bot_depth, mode=difficulty)
        self.pass_count = 0
        self.game_over = False
        self.board_history = []

        self.canvas.bind("<Button-1>", self.on_board_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)

        # --- Lógica de Início do Bot ---
        if self.game_mode == 'BvB':
            self.after(500, self.start_bot_thread)
        elif self.game_mode == 'HvB' and self.player_color == 'white':
            # CONDIÇÃO SOLICITADA: Jogador vs Bot e Jogador escolheu Branco (Bot começa)
            # Toca o som "bot_start" que é o som de mexer na caixa
            self.play_sound("bot_start")
            # Damos um tempo maior (2s) para o áudio tocar antes do bot jogar a primeira peça
            self.after(2000, self.start_bot_thread)

    # --- FUNÇÃO DE SOM ATUALIZADA (PYGAME) ---
    def play_sound(self, sound_type="move"):
        if not self.sound_enabled: return

        try:
            if sound_type == "move" and "move" in self.sounds:
                self.sounds["move"].play()
            elif sound_type == "bot_start" and "bot_start" in self.sounds:
                self.sounds["bot_start"].play()
            elif sound_type == "capture" or sound_type == "pass":
                # Como não temos arquivos específicos para captura/passar,
                # podemos usar o som de move ou manter o beep apenas para esses casos se desejar.
                # Aqui usarei o som de pedra padrão para simplificar.
                if "move" in self.sounds:
                    self.sounds["move"].play()
        except Exception as e:
            print(f"Erro ao tocar som: {e}")

    def start_bot_thread(self):
        if self.game_over or self.scoring_mode: return
        self.is_thinking = True
        self.config(cursor="watch")
        self.status_label.config(text="Bot pensando...", fg="blue")
        self.pass_btn.config(state="disabled")
        self.undo_btn.config(state="disabled")
        threading.Thread(target=self.run_bot_logic, daemon=True).start()

    def run_bot_logic(self):
        move = self.bot.escolher_jogada(self.stones, self.current_player, self.board_history)
        self.after(0, lambda: self.finish_bot_turn(move))

    def finish_bot_turn(self, move):
        self.is_thinking = False
        self.config(cursor="")
        self.pass_btn.config(state="normal")
        self.undo_btn.config(state="normal")
        if move:
            i, j = move
            if self.execute_move(i, j):
                self.pass_count = 0
            else:
                self.bot_pass()
        else:
            self.bot_pass()
        if self.game_mode == 'BvB' and not self.game_over:
            self.after(500, self.start_bot_thread)

    def on_board_click(self, event):
        if self.is_thinking: return
        if self.game_mode == 'BvB' and not self.scoring_mode: return
        x, y = event.x - self.offset + (self.cell_size // 2), event.y - self.offset + (self.cell_size // 2)
        i = x // self.cell_size
        j = y // self.cell_size
        if not (0 <= i < self.size and 0 <= j < self.size): return
        if self.scoring_mode:
            self.toggle_dead_stone(i, j)
        elif not self.game_over:
            if self.game_mode == 'HvB' and self.current_player != self.player_color: return
            self.canvas.delete("ghost")
            if self.execute_move(i, j):
                self.pass_count = 0
                if self.game_mode == 'HvB': self.after(100, self.start_bot_thread)

    def execute_move(self, i, j):
        if self.stones[i][j] != '': return False
        self.status_label.config(text="")
        temp_stones = [row[:] for row in self.stones]
        temp_stones[i][j] = self.current_player
        captured_count, new_board_state = self.simulate_captures(temp_stones, i, j)

        if not captured_count and self.is_suicide(new_board_state, i, j): return False

        for state in self.board_history:
            if new_board_state == state['stones']: return False

        # --- TOCAR SOM DA PEDRA ---
        self.play_sound("move")

        state_snapshot = {
            'stones': [row[:] for row in self.stones],
            'captures': self.captures.copy(),
            'current_player': self.current_player,
            'last_move': self.last_move
        }
        self.board_history.append(state_snapshot)
        self.stones = new_board_state
        self.captures[self.current_player] += captured_count
        self.last_move = (i, j)
        self.redraw_board_stones()
        self.score_label.config(text=self.get_score_text())
        self.total_moves += 1
        if self.total_moves >= self.max_moves:
            messagebox.showinfo("Limite", "Limite de turnos atingido.")
            self.initiate_scoring_phase()
            return True
        self.change_turn()
        return True

    def draw_stone_3d(self, i, j, color):
        cx, cy = self.offset + self.cell_size * i, self.offset + self.cell_size * j
        r = (self.cell_size // 2) - 2
        if (i, j) in self.dead_stones:
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="", stipple="gray50",
                                    tags="stone")
            return
        self.canvas.create_oval(cx - r + 2, cy - r + 2, cx + r + 2, cy + r + 2, fill="black", outline="",
                                stipple="gray25", tags="stone")
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="", tags="stone")
        if color == "black":
            self.canvas.create_oval(cx - r / 2, cy - r / 2, cx - r / 4, cy - r / 4, fill="gray30", outline="",
                                    tags="stone")
        else:
            self.canvas.create_oval(cx - r / 1.5, cy - r / 1.5, cx + r / 1.5, cy + r / 1.5, fill="#f0f0f0", outline="",
                                    tags="stone")
        if self.last_move == (i, j):
            marker_color = "white" if color == "black" else "black"
            mr = r // 2.5
            self.canvas.create_oval(cx - mr, cy - mr, cx + mr, cy + mr, outline=marker_color, width=2, tags="stone")

    def get_score_text(self):
        return (f"PLACAR\nPreto: {self.captures['black']}\nBranco: {self.captures['white']}\nKomi:  {self.komi}")

    def draw_board_grid(self):
        limit = self.offset + self.cell_size * (self.size - 1)
        if not self.board_image:
            self.canvas.create_rectangle(self.offset - 5, self.offset - 5, limit + 5, limit + 5, width=2,
                                         outline="#5d4037")
        letters = "ABCDEFGHJKLMNOPQRST"
        for i in range(self.size):
            pos = self.offset + self.cell_size * i
            self.canvas.create_line(self.offset, pos, limit, pos, fill="#3e2723", width=1)
            self.canvas.create_line(pos, self.offset, pos, limit, fill="#3e2723", width=1)
            self.canvas.create_text(self.offset - 20, pos, text=str(i + 1), font=("Arial", 9, "bold"), fill="#5d4037")
            if i < len(letters):
                self.canvas.create_text(pos, self.offset - 20, text=letters[i], font=("Arial", 9, "bold"),
                                        fill="#5d4037")
        stars = []
        if self.size == 9:
            stars = [(2, 2), (6, 2), (4, 4), (2, 6), (6, 6)]
        elif self.size == 13:
            stars = [(3, 3), (9, 3), (6, 6), (3, 9), (9, 9)]
        elif self.size == 19:
            stars = [(3, 3), (9, 3), (15, 3), (3, 9), (9, 9), (15, 9), (3, 15), (9, 15), (15, 15)]
        for sx, sy in stars:
            cx, cy = self.offset + self.cell_size * sx, self.offset + self.cell_size * sy
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="black")

    def on_mouse_move(self, event):
        if self.is_thinking or self.game_over or self.scoring_mode: return
        if self.game_mode == 'BvB': return
        if self.game_mode == 'HvB' and self.current_player != self.player_color: return
        x, y = event.x - self.offset + (self.cell_size // 2), event.y - self.offset + (self.cell_size // 2)
        i, j = x // self.cell_size, y // self.cell_size
        self.canvas.delete("ghost")
        if 0 <= i < self.size and 0 <= j < self.size and self.stones[i][j] == '':
            color = self.current_player if self.game_mode == 'HvH' else self.player_color
            cx, cy = self.offset + self.cell_size * i, self.offset + self.cell_size * j
            r = (self.cell_size // 2) - 2
            outline = "black" if color == "white" else ""
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline=outline, stipple="gray50",
                                    tags="ghost")

    def on_mouse_leave(self, event):
        self.canvas.delete("ghost")

    def give_hint(self):
        if self.game_over or self.scoring_mode or self.is_thinking: return
        self.status_label.config(text="Calculando dica...", fg="orange")
        self.config(cursor="watch")
        self.update()
        move = self.bot.escolher_jogada(self.stones, self.current_player, self.board_history)
        self.config(cursor="")
        self.status_label.config(text="")
        if move:
            i, j = move
            if self.execute_move(i, j):
                self.pass_count = 0
                if self.game_mode == 'HvB': self.after(100, self.start_bot_thread)
        else:
            messagebox.showinfo("Dica", "O Bot sugere passar a vez.")

    def bot_turn(self):
        pass

    def human_pass(self):
        if self.game_over or self.scoring_mode or self.is_thinking: return
        if self.game_mode == 'BvB': return
        if self.game_mode == 'HvB' and self.current_player != self.player_color: return
        self.play_sound("pass")
        self.status_label.config(text="")
        self.pass_count += 1
        self.last_move = None
        self.redraw_board_stones()
        self.change_turn()
        if self.pass_count >= 2:
            self.initiate_scoring_phase()
        else:
            if self.game_mode == 'HvB': self.after(100, self.start_bot_thread)

    def bot_pass(self):
        self.play_sound("pass")
        self.status_label.config(text="⚠️ O Bot Passou a Vez!", fg="#C0392B")
        self.pass_count += 1
        self.last_move = None
        self.redraw_board_stones()
        self.change_turn()
        if self.pass_count >= 2: self.initiate_scoring_phase()

    def undo_move(self):
        if self.game_over or self.scoring_mode or self.is_thinking: return
        steps = 1 if self.game_mode == 'HvH' else 2
        if len(self.board_history) >= steps:
            for _ in range(steps - 1): self.board_history.pop()
            target = self.board_history.pop()
            self.stones = target['stones']
            self.captures = target['captures']
            self.current_player = target['current_player']
            self.last_move = target['last_move']
            self.redraw_board_stones()
            self.score_label.config(text=self.get_score_text())
            self.label_turn.config(text=f"Vez: {'Preto' if self.current_player == 'black' else 'Branco'}")

    def simulate_captures(self, board, i, j):
        opponent = 'white' if self.current_player == 'black' else 'black'
        captures = 0;
        stones_to_remove = set()
        for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if 0 <= x < self.size and 0 <= y < self.size and board[x][y] == opponent:
                group = self.get_group(board, x, y)
                if self.is_group_dead(board, group):
                    for gx, gy in group: stones_to_remove.add((gx, gy))
        captures = len(stones_to_remove)
        new_board = [row[:] for row in board]
        for rx, ry in stones_to_remove: new_board[rx][ry] = ''
        return captures, new_board

    def is_suicide(self, board, i, j):
        return self.is_group_dead(board, self.get_group(board, i, j))

    def is_group_dead(self, board, group):
        for x, y in group:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if board[nx][ny] == '': return False
        return True

    def get_group(self, board, i, j):
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

    def change_turn(self):
        self.current_player = 'white' if self.current_player == 'black' else 'black'
        self.label_turn.config(text=f"Vez: {'Preto' if self.current_player == 'black' else 'Branco'}")

    def initiate_scoring_phase(self):
        self.scoring_mode = True
        self.label_turn.config(text="Marcar mortos")
        messagebox.showinfo("Fim", "Jogo finalizado.\nClique nas pedras mortas para removê-las antes de confirmar.")
        self.pass_btn.pack_forget();
        self.undo_btn.pack_forget();
        self.hint_btn.pack_forget()
        self.finish_btn.pack(pady=20, fill=tk.X)

    def toggle_dead_stone(self, i, j):
        if self.stones[i][j] == '': return
        group = self.get_group(self.stones, i, j)
        is_dead = (i, j) in self.dead_stones
        for gx, gy in group:
            if is_dead:
                self.dead_stones.discard((gx, gy))
            else:
                self.dead_stones.add((gx, gy))
        self.redraw_board_stones()

    def calculate_final_score(self):
        self.game_over = True
        final_board = [row[:] for row in self.stones]
        extra_b, extra_w = 0, 0
        for r, c in self.dead_stones:
            if final_board[r][c] == 'white':
                extra_b += 1
            elif final_board[r][c] == 'black':
                extra_w += 1
            final_board[r][c] = ''
        black_terr, white_terr, b_coords, w_coords = self.calculate_territory_map(final_board)
        self.draw_territory(b_coords, w_coords)
        final_black = black_terr + self.captures['black'] + extra_b
        final_white = white_terr + self.captures['white'] + extra_w + self.komi
        if self.rules == 'Chinesa':
            stones_b = sum(row.count('black') for row in final_board)
            stones_w = sum(row.count('white') for row in final_board)
            final_black = black_terr + stones_b
            final_white = white_terr + stones_w + self.komi
        msg = f"Preto: {final_black}\nBranco: {final_white}\n\nVencedor: {'PRETO' if final_black > final_white else 'BRANCO'}"
        messagebox.showinfo("Resultado", msg)
        self.destroy()
        from menu import MainMenu
        menu = MainMenu()
        menu.mainloop()

    def calculate_territory_map(self, board):
        black_terr, white_terr = 0, 0
        b_coords, w_coords = set(), set()
        visited = set()
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == '' and (i, j) not in visited:
                    group, owners = self.flood_fill(board, i, j, visited)
                    if len(owners) == 1:
                        owner = owners.pop()
                        if owner == 'black':
                            black_terr += len(group);
                            b_coords.update(group)
                        else:
                            white_terr += len(group);
                            w_coords.update(group)
        return black_terr, white_terr, b_coords, w_coords

    def flood_fill(self, board, i, j, visited):
        stack = [(i, j)];
        group = set();
        owners = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in visited: continue
            visited.add((x, y));
            group.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if board[nx][ny] == '':
                        if (nx, ny) not in visited: stack.append((nx, ny))
                    else:
                        owners.add(board[nx][ny])
        return group, owners

    def redraw_board_stones(self):
        self.canvas.delete("stone");
        self.canvas.delete("territory")
        for i in range(self.size):
            for j in range(self.size):
                if self.stones[i][j] != '': self.draw_stone_3d(i, j, self.stones[i][j])

    def draw_territory(self, b_coords, w_coords):
        tr = self.cell_size // 5
        for i, j in b_coords:
            cx, cy = self.offset + self.cell_size * i, self.offset + self.cell_size * j
            self.canvas.create_rectangle(cx - tr, cy - tr, cx + tr, cy + tr, fill="black", outline="", tags="territory")
        for i, j in w_coords:
            cx, cy = self.offset + self.cell_size * i, self.offset + self.cell_size * j
            self.canvas.create_rectangle(cx - tr, cy - tr, cx + tr, cy + tr, fill="white", outline="black",
                                         tags="territory")


if __name__ == "__main__":
    app = GoBoard()
    app.mainloop()