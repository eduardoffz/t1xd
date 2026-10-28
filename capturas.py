# capturas.py — Integrante 3: Rei, Cavalo e Capturas
# Importa apenas de tabuleiro.py

from tabuleiro import posicao_valida, obter_peca, cor_da_peca, mover_peca


def movimento_rei(origem, destino):
    """
    Verifica se o movimento do rei é válido (apenas geometria).
    O rei move uma casa em qualquer direção.
    Parâmetros:
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
    Retorna:
        bool
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    if origem == destino:
        return False

    dl = destino[0] - origem[0]
    dc = destino[1] - origem[1]

    # O rei move no máximo 1 casa em qualquer direção
    if max(abs(dl), abs(dc)) == 1:
        return True
    return False


def movimento_cavalo(origem, destino):
    """
    Verifica se o movimento do cavalo é válido (apenas geometria).
    O cavalo move em 'L': 2 casas em uma direção e 1 na outra.
    Parâmetros:
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
    Retorna:
        bool
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    if origem == destino:
        return False

    dl = abs(destino[0] - origem[0])
    dc = abs(destino[1] - origem[1])

    # Movimento em L: (1,2) ou (2,1)
    if (dl == 1 and dc == 2) or (dl == 2 and dc == 1):
        return True
    return False


def mesma_cor(peca1, peca2):
    """
    Verifica se duas peças são da mesma cor.
    Parâmetros:
        peca1 (str): primeira peça.
        peca2 (str): segunda peça.
    Retorna:
        bool: True se ambas são peças (não vazias) e da mesma cor.
    """
    cor1 = cor_da_peca(peca1)
    cor2 = cor_da_peca(peca2)
    # Se qualquer uma for vazia, não é mesma cor
    if cor1 is None or cor2 is None:
        return False
    return cor1 == cor2


def captura_permitida(tab, origem, destino):
    """
    Verifica se uma captura é permitida.
    True somente se há peça na origem, peça no destino, e cores diferentes.
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
    Retorna:
        bool
    """
    peca_origem = obter_peca(tab, origem)
    peca_destino = obter_peca(tab, destino)

    # Origem vazia -> não há captura
    if peca_origem == ".":
        return False
    # Destino vazio -> não é captura
    if peca_destino == ".":
        return False
    # Mesma cor -> não pode capturar
    if mesma_cor(peca_origem, peca_destino):
        return False
    return True


def capturar_peca(tab, origem, destino):
    """
    Realiza a captura de uma peça (move a peça da origem para o destino,
    sobrescrevendo a peça adversária).
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
    Retorna:
        bool: True se a captura foi realizada.
    """
    if captura_permitida(tab, origem, destino):
        mover_peca(tab, origem, destino)
        return True
    return False

