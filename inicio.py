ROWS = 6
COLS = 7
MAX_DEPTH = 4  # Profundidade do Minimax (aumente para IA mais forte, mas mais lenta)

def criar_tabuleiro():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def imprimir_tabuleiro(tab):
    simbolos = {0: ' ', 1: '★', 2: '●'}  #maquina bolinha, eu estrela
    for linha in tab:
        print('|' + '|'.join(simbolos[x] for x in linha) + '|')
    print('-' * (COLS * 2 + 1))

def coluna_valida(tab, col):
    return tab[0][col] == 0

def fazer_jogada(tab, col, jogador):
    for i in range(ROWS-1, -1, -1): #comeca de baixo pra cima
        if tab[i][col] == 0:
            tab[i][col] = jogador #se ta vazio coloca o simbolo do jogador
            return True
    return False

def desfazer_jogada(tab, col):
    for i in range(ROWS):
        if tab[i][col] != 0:
            tab[i][col] = 0
            return

def verificar_vencedor(tab, jogador):
    # Horizontal, ve se fez 4 pontos 
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(tab[r][c+i] == jogador for i in range(4)):
                return True
            
    # Vertical, ve se fez 4 pontos
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(tab[r+i][c] == jogador for i in range(4)):
                return True
            
    # Diagonal / da esquerda para direita de baixo para cima
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(tab[r - i][c + i] == jogador for i in range(4)):
                return True
            
    # Diagonal \ da esquerda para direita de cima para baixo
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(tab[r + i][c + i] == jogador for i in range(4)):
                return True
    return False

def tabuleiro_cheio(tab):
    return all(tab[0][c] != 0 for c in range(COLS))

def avaliar_janela(janela, jogador):
    # Avalia uma janela de 4 posições para heurística
    pontuacao = 0
    oponente = 1 if jogador == 2 else 2

    if janela.count(jogador) == 4:
        pontuacao += 100
    elif janela.count(jogador) == 3 and janela.count(0) == 1:
        pontuacao += 5
    elif janela.count(jogador) == 2 and janela.count(0) == 2:
        pontuacao += 2

    if janela.count(oponente) == 3 and janela.count(0) == 1:
        pontuacao -= 4

    return pontuacao

def avaliar_tabuleiro(tab, jogador):
    pontuacao = 0

    # Centro (prioriza coluna do meio)
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
    oponente = 1 if jogador == 2 else 2

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
                    break
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
                    break
        return melhor_coluna, valor_min

def melhor_jogada(tab, jogador):
    coluna, _ = minimax(tab, MAX_DEPTH, -float('inf'), float('inf'), True, jogador)
    return coluna

def jogo():
    tab = criar_tabuleiro()
    jogador_humano = 1
    jogador_ia = 2
    jogador_atual = 1

    while True:
        imprimir_tabuleiro(tab)

        if jogador_atual == jogador_humano:
            try:
                col = int(input("Sua jogada (0-6): "))
            except:
                print("Entrada inválida. Tente novamente.")
                continue
            if col < 0 or col >= COLS or not coluna_valida(tab, col):
                print("Jogada inválida. Tente novamente.")
                continue
        else:
            print("Computador pensando...")
            col = melhor_jogada(tab, jogador_ia)
            print(f"Computador jogou na coluna {col}")

        fazer_jogada(tab, col, jogador_atual)

        if verificar_vencedor(tab, jogador_atual):
            imprimir_tabuleiro(tab)
            if jogador_atual == jogador_humano:
                print("Parabéns! Você venceu!")
            else:
                print("Computador venceu!")
            break

        if tabuleiro_cheio(tab):
            imprimir_tabuleiro(tab)
            print("Empate!")
            break

        jogador_atual = 2 if jogador_atual == 1 else 1

if __name__ == "__main__":
    jogo()
