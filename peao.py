# peao.py — Integrante 4: Peão, Turnos
# Importa apenas de tabuleiro.py

from tabuleiro import posicao_valida, obter_peca, cor_da_peca


def movimento_peao(tab, origem, destino):
    """
    Verifica se o movimento do peão é válido.
    Considera direção, avanço de 1 ou 2 casas, e captura diagonal.
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
    Retorna:
        bool
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    if origem == destino:
        return False

    peca = obter_peca(tab, origem)
    if peca == ".":
        return False

    cor = cor_da_peca(peca)
    # Determina direção e linha inicial conforme a cor
    if cor == "b":
        direcao = -1       # brancas sobem (linha diminui)
        linha_inicial = 6
    elif cor == "p":
        direcao = 1        # pretas descem (linha aumenta)
        linha_inicial = 1
    else:
        return False

    dl = destino[0] - origem[0]
    dc = destino[1] - origem[1]

    # Movimento reto (sem mudar de coluna)
    if dc == 0:
        # Avançar 1 casa
        if dl == direcao:
            if obter_peca(tab, destino) == ".":
                return True
            return False
        # Avançar 2 casas (só da linha inicial)
        if dl == 2 * direcao:
            if origem[0] == linha_inicial:
                # Verifica casa do meio e destino vazias
                casa_meio = (origem[0] + direcao, origem[1])
                if obter_peca(tab, casa_meio) == "." and obter_peca(tab, destino) == ".":
                    return True
            return False
        # Qualquer outro deslocamento vertical sem mudar coluna é inválido
        return False

    # Captura diagonal
    if abs(dc) == 1 and dl == direcao:
        peca_destino = obter_peca(tab, destino)
        # Só pode capturar peça de cor oposta
        if peca_destino != "." and cor_da_peca(peca_destino) != cor:
            return True
        return False

    # Qualquer outra combinação é inválida
    return False


def controlar_turno(turno, peca):
    """
    Verifica se a peça pertence ao jogador do turno atual.
    Parâmetros:
        turno (str): 'brancas' ou 'pretas'.
        peca (str): string da peça (ex: 'Pb').
    Retorna:
        bool: True se a peça pertence ao jogador do turno.
    """
    if peca == ".":
        return False
    cor = cor_da_peca(peca)
    if turno == "brancas" and cor == "b":
        return True
    if turno == "pretas" and cor == "p":
        return True
    return False


def trocar_turno(turno):
    """
    Troca o turno de jogo.
    Parâmetros:
        turno (str): 'brancas' ou 'pretas'.
    Retorna:
        str: o turno oposto.
    """
    if turno == "brancas":
        return "pretas"
    return "brancas"

