# Regras do Jogo de Go

O Go é um jogo de estratégia territorial para dois jogadores. O objetivo principal é cercar mais território que o oponente. Abaixo estão as regras fundamentais para jogar e pontuar.

---

### 1. Início do Jogo e Komi
* **A Vez:** O jogador com as pedras **Pretas** sempre começa o jogo.
* **Komi (Compensação):** Como as Pretas têm a vantagem da iniciativa por jogar primeiro, o jogador com as pedras **Brancas** recebe uma compensação em pontos adicionada ao seu placar final.
    * *Valor:* Geralmente, o Komi é de **6.5 pontos**. O meio ponto (0.5) serve para evitar empates.

### 2. Mecânica de Captura
* **Liberdades:** Cada pedra colocada no tabuleiro tem "liberdades", que são as interseções vazias adjacentes (acima, abaixo, esquerda e direita).
* **Captura:** Uma pedra (ou grupo de pedras conectadas) é capturada quando perde sua última liberdade, ou seja, quando está totalmente cercada por pedras inimigas. As pedras capturadas são retiradas do tabuleiro e tornam-se "prisioneiros".
* **Suicídio:** É **proibido** colocar uma pedra em um local onde ela ficaria imediatamente sem liberdades (cercada), a menos que essa jogada resulte na captura imediata de pedras do oponente.

### 3. Regras Especiais de Situação
* **Regra Ko:** Para evitar ciclos infinitos, é proibido fazer uma jogada que retorne o tabuleiro **exatamente** à posição anterior. Se uma pedra for capturada e criar essa situação ("Ko"), o oponente deve jogar em outro lugar antes de poder recapturar naquela posição.
* **Seki (Vida Mútua):** Ocorre quando grupos de pedras opostas compartilham liberdades, mas nenhum dos jogadores pode preencher essas liberdades sem colocar o próprio grupo em perigo de captura imediata. Essas pedras são consideradas vivas, mas **não contam como território** na regra japonesa.

### 4. Condições de Fim de Jogo
O jogo não termina pela captura do rei (como no Xadrez), mas por acordo mútuo:
1.  Quando um jogador acredita que não há mais jogadas valiosas (que ganhem território ou reduzam o do oponente), ele diz **"Passo"**.
2.  Se ambos os jogadores passarem consecutivamente, o jogo termina.
3.  **Fase de Remoção:** Após o fim do jogo, os jogadores identificam as "pedras mortas" (pedras que ficaram no tabuleiro mas não têm chance de sobreviver/fazer dois olhos). Estas são removidas e contadas como prisioneiros.

---

### 5. Contagem de Pontos (Sistemas de Regras)

Existem duas formas principais de contar os pontos. O resultado geralmente é o mesmo, mas o método difere.

#### **A. Regra Japonesa (Território + Prisioneiros)**
É a regra mais comum em torneios internacionais e servidores online. O foco está na eficiência.
* **Território:** Conta-se cada interseção vazia cercada exclusivamente por um jogador.
* **Prisioneiros:** Somam-se as pedras inimigas capturada durante o jogo + as pedras mortas retiradas no final.
* **Cálculo:**
    > Pontuação = (Território Controlado) + (Prisioneiros Inimigos) + (Komi, se for Branco).

#### **B. Regra Chinesa (Área)**
O foco está na ocupação física do tabuleiro.
* **Área:** Conta-se cada interseção vazia cercada **MAIS** cada pedra viva do próprio jogador que está no tabuleiro.
* **Cálculo:**
    > Pontuação = (Território Controlado) + (Pedras Vivas no Tabuleiro) + (Komi, se for Branco).

---

### Glossário Rápido
* **Atari:** Estado em que uma pedra ou grupo tem apenas uma liberdade restante (está prestes a ser capturado).
* **Olhos:** Espaços vazios internos que garantem a vida de um grupo. Um grupo com dois olhos separados é imortal.
* **Dame:** Pontos neutros entre as fronteiras dos jogadores que não valem território para ninguém.