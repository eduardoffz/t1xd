# pecas_linha.py — Integrante 2: Torre, Bispo, Dama
# Importa apenas de tabuleiro.py

from tabuleiro import posicao_valida


def caminho_livre(tab, origem, destino):
    """
    Verifica se todas as casas entre origem e destino estão vazias.
    Funciona para linhas retas (horizontal, vertical) e diagonais.
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem (linha, coluna).
        destino (tuple): posição de destino (linha, coluna).
    Retorna:
        bool: True se o caminho está livre.
    """
    dl = destino[0] - origem[0]
    dc = destino[1] - origem[1]

    # Verifica se está na mesma linha, coluna ou diagonal
    if dl != 0 and dc != 0 and abs(dl) != abs(dc):
        return False

    # Calcula o passo em cada direção (-1, 0 ou +1)
    if dl > 0:
        passo_l = 1
    elif dl < 0:
        passo_l = -1
    else:
        passo_l = 0

    if dc > 0:
        passo_c = 1
    elif dc < 0:
        passo_c = -1
    else:
        passo_c = 0

    # Percorre as casas intermediárias (sem incluir origem e destino)
    l = origem[0] + passo_l
    c = origem[1] + passo_c
    while (l, c) != destino:
        if tab[l][c] != ".":
            return False
        l = l + passo_l
        c = c + passo_c
    return True


def movimento_torre(origem, destino, tab=None):
    """
    Verifica se o movimento da torre é válido.
    Parâmetros:
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
        tab (list): tabuleiro (opcional; se None, só checa a geometria).
    Retorna:
        bool
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    if origem == destino:
        return False

    dl = destino[0] - origem[0]
    dc = destino[1] - origem[1]

    # A torre move em linha reta: mesma linha ou mesma coluna
    if dl != 0 and dc != 0:
        return False

    # Se o tabuleiro foi passado, verifica obstrução
    if tab is not None:
        if not caminho_livre(tab, origem, destino):
            return False

    return True


def movimento_bispo(origem, destino, tab=None):
    """
    Verifica se o movimento do bispo é válido.
    Parâmetros:
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
        tab (list): tabuleiro (opcional; se None, só checa a geometria).
    Retorna:
        bool
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    if origem == destino:
        return False

    dl = destino[0] - origem[0]
    dc = destino[1] - origem[1]

    # O bispo move na diagonal: abs(dl) deve ser igual a abs(dc)
    if abs(dl) != abs(dc):
        return False

    # Se o tabuleiro foi passado, verifica obstrução
    if tab is not None:
        if not caminho_livre(tab, origem, destino):
            return False

    return True


def movimento_dama(origem, destino, tab=None):
    """
    Verifica se o movimento da dama é válido.
    A dama combina os movimentos da torre e do bispo.
    Parâmetros:
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
        tab (list): tabuleiro (opcional; se None, só checa a geometria).
    Retorna:
        bool
    """
    # Reaproveita as funções da torre e do bispo
    if movimento_torre(origem, destino, tab):
        return True
    if movimento_bispo(origem, destino, tab):
        return True
    return False

