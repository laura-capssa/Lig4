# Jogo Lig4 (Conecta 4) com IA usando Minimax
# -------------------------------------------------
# Este script implementa o jogo Lig4 (também conhecido como Conecta 4),
# permitindo que um jogador humano jogue contra o computador (IA).
# A IA utiliza o algoritmo Minimax com poda Alpha-Beta para decidir suas jogadas.

# Constantes do jogo
ROWS = 6         # Número de linhas do tabuleiro
COLS = 7         # Número de colunas do tabuleiro
MAX_DEPTH = 4    # Profundidade máxima do Minimax (aumente para IA mais forte, mas mais lenta)

def criar_tabuleiro():
    """Cria e retorna um tabuleiro vazio (matriz 6x7 preenchida com zeros)."""
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def imprimir_tabuleiro(tab):
    """
    Imprime o tabuleiro no console.
    0 = vazio, 1 = jogador humano (★), 2 = computador (●)
    """
    simbolos = {0: ' ', 1: '★', 2: '●'}  # máquina bolinha, eu estrela
    for linha in tab:
        print('|' + '|'.join(simbolos[x] for x in linha) + '|')
    print('-' * (COLS * 2 + 1)) 

def coluna_valida(tab, col):
    """
    Verifica se a coluna escolhida é válida (a célula do topo está vazia).
    Retorna True se for possível jogar na coluna, False caso contrário.
    """
    return tab[0][col] == 0

def fazer_jogada(tab, col, jogador):
    """
    Realiza a jogada do jogador na coluna escolhida.
    Preenche a célula mais baixa disponível na coluna.
    Retorna True se a jogada foi realizada, False se a coluna está cheia.
    """
    for i in range(ROWS-1, -1, -1):  # começa de baixo pra cima
        if tab[i][col] == 0:
            tab[i][col] = jogador  # coloca o símbolo do jogador
            return True
    return False  # se a coluna está cheia

def desfazer_jogada(tab, col):
    """
    Desfaz a última jogada feita em uma coluna (usado pelo Minimax para simulação).
    Remove o topo da coluna.
    """
    for i in range(ROWS):
        if tab[i][col] != 0:
            tab[i][col] = 0
            return

def verificar_vencedor(tab, jogador):
    """
    Verifica se o jogador venceu (4 peças seguidas em linha, coluna ou diagonal).
    Retorna True se o jogador venceu, False caso contrário.
    """
    # Horizontal 
    for r in range(ROWS):
        for c in range(COLS - 3):  # verifica todas as sequências de 4 colunas
            if all(tab[r][c+i] == jogador for i in range(4)):
                return True
            
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(tab[r+i][c] == jogador for i in range(4)):
                return True
            
    # Diagonal / (da esquerda para direita de baixo para cima)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(tab[r - i][c + i] == jogador for i in range(4)):
                return True
            
    # Diagonal \ (da esquerda para direita de cima para baixo)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(tab[r + i][c + i] == jogador for i in range(4)):
                return True
    return False

def tabuleiro_cheio(tab):
    """
    Verifica se o tabuleiro está cheio (todas as colunas do topo ocupadas).
    Retorna True se não há mais jogadas possíveis.
    """
    return all(tab[0][c] != 0 for c in range(COLS))

def avaliar_janela(janela, jogador):
    """
    Avalia uma janela (lista de 4 posições) para a heurística do Minimax.
    Retorna uma pontuação baseada na quantidade de peças do jogador e do oponente.
    """
    pontuacao = 0
    oponente = 1 if jogador == 2 else 2

    if janela.count(jogador) == 4:
        pontuacao += 100  # vitória iminente

    elif janela.count(jogador) == 3 and janela.count(0) == 1:
        pontuacao += 5    # três peças e uma vaga

    elif janela.count(jogador) == 2 and janela.count(0) == 2:
        pontuacao += 2    # duas peças e duas vagas

    if janela.count(oponente) == 3 and janela.count(0) == 1:
        pontuacao -= 4    # bloqueia o oponente

    return pontuacao

def avaliar_tabuleiro(tab, jogador):
    """
    Avalia o tabuleiro inteiro para o jogador atual.
    Soma pontuações de todas as possíveis janelas de 4 posições.
    """
    pontuacao = 0

    # Prioriza o centro (mais chances de formar linhas)
    centro = [tab[r][COLS//2] for r in range(ROWS)]
    pontuacao += centro.count(jogador) * 3

    # Horizontal
    for r in range(ROWS):
        linha = tab[r]
        for c in range(COLS - 3):
            janela = linha[c:c+4]
            pontuacao += avaliar_janela(janela, jogador)

    # Vertical
    for c in range(COLS):
        coluna = [tab[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            janela = coluna[r:r+4]
            pontuacao += avaliar_janela(janela, jogador)

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            janela = [tab[r - i][c + i] for i in range(4)]
            pontuacao += avaliar_janela(janela, jogador)

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            janela = [tab[r + i][c + i] for i in range(4)]
            pontuacao += avaliar_janela(janela, jogador)

    return pontuacao

def minimax(tab, profundidade, alpha, beta, maximizar, jogador):
    """
    Algoritmo Minimax com poda Alpha-Beta.
    Retorna a melhor coluna e o valor da avaliação para o jogador.
    """
    oponente = 1 if jogador == 2 else 2

    # Condições de parada: vitória, derrota, empate ou profundidade máxima
    if verificar_vencedor(tab, jogador):
        return (None, 1000000)
    elif verificar_vencedor(tab, oponente):
        return (None, -1000000)
    elif tabuleiro_cheio(tab) or profundidade == 0:
        return (None, avaliar_tabuleiro(tab, jogador))

    if maximizar:
        valor_max = -float('inf')
        melhor_coluna = None
        for col in range(COLS):
            if coluna_valida(tab, col):
                fazer_jogada(tab, col, jogador)
                _, valor = minimax(tab, profundidade -1, alpha, beta, False, jogador)
                desfazer_jogada(tab, col)
                if valor > valor_max:
                    valor_max = valor
                    melhor_coluna = col
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break  # poda beta
        return melhor_coluna, valor_max
    else:
        valor_min = float('inf')
        melhor_coluna = None
        for col in range(COLS):
            if coluna_valida(tab, col):
                fazer_jogada(tab, col, oponente)
                _, valor = minimax(tab, profundidade -1, alpha, beta, True, jogador)
                desfazer_jogada(tab, col)
                if valor < valor_min:
                    valor_min = valor
                    melhor_coluna = col
                beta = min(beta, valor)
                if alpha >= beta:
                    break  # poda alpha
        return melhor_coluna, valor_min

def melhor_jogada(tab, jogador):
    """
    Retorna a melhor coluna para o jogador atual usando o Minimax.
    """
    coluna, _ = minimax(tab, MAX_DEPTH, -float('inf'), float('inf'), True, jogador)
    return coluna

def jogo():
    """
    Função principal que executa o loop do jogo.
    Alterna entre o jogador humano e o computador até o fim do jogo.
    """
    tab = criar_tabuleiro()
    jogador_humano = 1
    jogador_ia = 2
    jogador_atual = 1

    while True:
        imprimir_tabuleiro(tab)

        if jogador_atual == jogador_humano:
            # Turno do jogador humano
            try:
                col = int(input("Sua jogada (0-6): "))
            except:
                print("Entrada inválida. Tente novamente.")
                continue
            if col < 0 or col >= COLS or not coluna_valida(tab, col):
                print("Jogada inválida. Tente novamente.")
                continue
        else:
            # Turno do computador (IA)
            print("Computador pensando...")
            col = melhor_jogada(tab, jogador_ia)
            print(f"Computador jogou na coluna {col}")

        fazer_jogada(tab, col, jogador_atual)

        # Verifica se houve vencedor
        if verificar_vencedor(tab, jogador_atual):
            imprimir_tabuleiro(tab)
            if jogador_atual == jogador_humano:
                print("Parabéns! Você venceu!")
            else:
                print("Computador venceu!")
            break

        # Verifica empate
        if tabuleiro_cheio(tab):
            imprimir_tabuleiro(tab)
            print("Empate!")
            break

        # Alterna o jogador
        jogador_atual = 2 if jogador_atual == 1 else 1

if __name__ == "__main__":
    # Inicia o jogo se o script for executado diretamente
    jogo()
