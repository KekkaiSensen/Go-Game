import tkinter as tk
from game import GoBoard  # Importa a classe do jogo

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Principal - Go Game")
        self.geometry("400x550") # Aumentei altura para caber novas opções
        self.configure(bg="#2C3E50")

        # --- Variáveis de Configuração ---
        self.difficulty_var = tk.StringVar(value="Médio")
        self.color_var = tk.StringVar(value="black")
        self.size_var = tk.IntVar(value=13)
        self.rules_var = tk.StringVar(value="Japonesa")
        self.mode_var = tk.StringVar(value="HvB") # HvB, HvH, BvB

        # Título
        lbl_title = tk.Label(self, text="GO GAME", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="white")
        lbl_title.pack(pady=20)

        # Botões Principais
        btn_play = tk.Button(self, text="JOGAR", font=("Arial", 14), width=15,
                             bg="#27AE60", fg="white", command=self.start_game)
        btn_play.pack(pady=10)

        btn_options = tk.Button(self, text="OPÇÕES", font=("Arial", 14), width=15,
                                bg="#2980B9", fg="white", command=self.open_options)
        btn_options.pack(pady=10)

        btn_exit = tk.Button(self, text="SAIR", font=("Arial", 12), width=15,
                             bg="#C0392B", fg="white", command=self.quit)
        btn_exit.pack(pady=30)

    def open_options(self):
        options_window = tk.Toplevel(self)
        options_window.title("Configurações")
        options_window.geometry("350x700")
        options_window.configure(bg="#ECF0F1")

        # --- Modo de Jogo (NOVO) ---
        tk.Label(options_window, text="Modo de Jogo:", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(15, 5))
        frame_mode = tk.Frame(options_window, bg="#ECF0F1")
        frame_mode.pack()
        tk.Radiobutton(frame_mode, text="Humano vs Bot", variable=self.mode_var, value="HvB", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_mode, text="Humano vs Humano", variable=self.mode_var, value="HvH", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_mode, text="Bot vs Bot (Spectator)", variable=self.mode_var, value="BvB", bg="#ECF0F1").pack(anchor=tk.W)

        # --- Dificuldade ---
        tk.Label(options_window, text="Dificuldade (Bot):", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(15, 5))
        frame_diff = tk.Frame(options_window, bg="#ECF0F1")
        frame_diff.pack()
        tk.Radiobutton(frame_diff, text="Fácil", variable=self.difficulty_var, value="Fácil", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_diff, text="Médio", variable=self.difficulty_var, value="Médio", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_diff, text="Difícil", variable=self.difficulty_var, value="Difícil", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_diff, text="Muito Difícil", variable=self.difficulty_var, value="Muito Difícil", bg="#ECF0F1", fg="red").pack(anchor=tk.W)

        # --- Tamanho do Tabuleiro ---
        tk.Label(options_window, text="Tamanho do Tabuleiro:", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(15, 5))
        frame_size = tk.Frame(options_window, bg="#ECF0F1")
        frame_size.pack()
        tk.Radiobutton(frame_size, text="9x9", variable=self.size_var, value=9, bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_size, text="13x13", variable=self.size_var, value=13, bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_size, text="19x19", variable=self.size_var, value=19, bg="#ECF0F1").pack(anchor=tk.W)

        # --- Regras ---
        tk.Label(options_window, text="Sistema de Regras:", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(15, 5))
        frame_rules = tk.Frame(options_window, bg="#ECF0F1")
        frame_rules.pack()
        tk.Radiobutton(frame_rules, text="Japonesa", variable=self.rules_var, value="Japonesa", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_rules, text="Chinesa", variable=self.rules_var, value="Chinesa", bg="#ECF0F1").pack(anchor=tk.W)

        # --- Cor ---
        tk.Label(options_window, text="Sua Cor (HvB):", font=("Arial", 11, "bold"), bg="#ECF0F1").pack(pady=(15, 5))
        frame_color = tk.Frame(options_window, bg="#ECF0F1")
        frame_color.pack()
        tk.Radiobutton(frame_color, text="Preto (Começa)", variable=self.color_var, value="black", bg="#ECF0F1").pack(anchor=tk.W)
        tk.Radiobutton(frame_color, text="Branco (Joga em 2º)", variable=self.color_var, value="white", bg="#ECF0F1").pack(anchor=tk.W)

        tk.Button(options_window, text="Salvar e Voltar", command=options_window.destroy, bg="#BDC3C7").pack(pady=30)

    def start_game(self):
        diff = self.difficulty_var.get()
        color = self.color_var.get()
        size = self.size_var.get()
        rules = self.rules_var.get()
        mode = self.mode_var.get()

        self.destroy()
        # Passa o 'mode' para o jogo
        game = GoBoard(size=size, difficulty=diff, player_color=color, rules=rules, game_mode=mode)
        game.mainloop()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()