import tkinter as tk
from tkinter import ttk
from game import GoBoard


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Principal - Go Game")
        self.geometry("400x600")
        self.configure(bg="#2C3E50")

        # --- Variáveis de Configuração ---
        self.difficulty_var = tk.StringVar(value="Médio")
        self.color_var = tk.StringVar(value="black")
        self.size_var = tk.IntVar(value=13)
        self.rules_var = tk.StringVar(value="Japonesa")
        self.mode_var = tk.StringVar(value="HvB")
        self.sound_var = tk.BooleanVar(value=True)

        # Título
        lbl_title = tk.Label(self, text="GO GAME", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="white")
        lbl_title.pack(pady=20)

        # Botões Principais
        # JOGAR (Fonte 14, Largura 15)
        btn_play = tk.Button(self, text="JOGAR", font=("Arial", 14), width=15,
                             bg="#27AE60", fg="white", command=self.start_game)
        btn_play.pack(pady=10)

        # OPÇÕES (Fonte 14, Largura 15)
        btn_options = tk.Button(self, text="OPÇÕES", font=("Arial", 14), width=15,
                                bg="#2980B9", fg="white", command=self.open_options)
        btn_options.pack(pady=10)

        # SAIR (Ajustado: Fonte 14, Largura 15)
        btn_exit = tk.Button(self, text="SAIR", font=("Arial", 14), width=15,
                             bg="#C0392B", fg="white", command=self.quit)
        btn_exit.pack(pady=30)

    # ... (O restante do código permanece igual)
    def open_options(self):
        # ... (código existente da função open_options)
        options_window = tk.Toplevel(self)
        options_window.title("Configurações")
        options_window.geometry("350x600")
        options_window.configure(bg="#ECF0F1")

        lbl_style = {"font": ("Arial", 11, "bold"), "bg": "#ECF0F1", "fg": "#2C3E50"}

        def create_dropdown(parent, label_text, variable, display_map):
            tk.Label(parent, text=label_text, **lbl_style).pack(pady=(15, 5))
            display_values = list(display_map.keys())
            inv_map = {v: k for k, v in display_map.items()}

            combo = ttk.Combobox(parent, values=display_values, state="readonly", font=("Arial", 10))
            combo.pack(pady=0, ipadx=5)

            current_val = variable.get()
            if current_val in inv_map:
                combo.set(inv_map[current_val])

            def on_select(event):
                selected_text = combo.get()
                internal_value = display_map[selected_text]
                variable.set(internal_value)

            combo.bind("<<ComboboxSelected>>", on_select)
            return combo

        create_dropdown(options_window, "Modo de Jogo:", self.mode_var, {
            "Humano vs Bot": "HvB",
            "Humano vs Humano": "HvH",
            "Bot vs Bot (Spectator)": "BvB"
        })

        create_dropdown(options_window, "Dificuldade (Bot):", self.difficulty_var, {
            "Fácil": "Fácil", "Médio": "Médio", "Difícil": "Difícil", "Muito Difícil": "Muito Difícil"
        })

        create_dropdown(options_window, "Tamanho do Tabuleiro:", self.size_var, {
            "9x9 (Rápido)": 9, "13x13 (Padrão)": 13, "19x19 (Profissional)": 19
        })

        create_dropdown(options_window, "Sistema de Regras:", self.rules_var, {
            "Japonesa (Território)": "Japonesa", "Chinesa (Área)": "Chinesa"
        })

        create_dropdown(options_window, "Sua Cor (HvB):", self.color_var, {
            "Preto (Começa Jogando)": "black", "Branco (Joga em 2º + Komi)": "white"
        })

        create_dropdown(options_window, "Efeitos Sonoros:", self.sound_var, {
            "Ligado": True, "Desligado": False
        })

        tk.Button(options_window, text="Salvar e Voltar", command=options_window.destroy,
                  bg="#BDC3C7", font=("Arial", 10)).pack(pady=30)

    def start_game(self):
        diff = self.difficulty_var.get()
        color = self.color_var.get()
        size = self.size_var.get()
        rules = self.rules_var.get()
        mode = self.mode_var.get()
        sound = self.sound_var.get()

        self.destroy()
        game = GoBoard(size=size, difficulty=diff, player_color=color,
                       rules=rules, game_mode=mode, sound_enabled=sound)
        game.mainloop()


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()