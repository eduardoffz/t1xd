# tabuleiro.py — Integrante 1: Estrutura e Tabuleiro
# Este arquivo NÃO importa nada do projeto.


def criar_tabuleiro():
    """
    Cria e retorna o tabuleiro inicial de xadrez (8x8).
    Retorna:
        list: matriz 8x8 com strings representando as peças.
    """
    # Linha 0: peças pretas (topo)
    # Linha 1: peões pretos
    # Linhas 2-5: casas vazias
    # Linha 6: peões brancos
    # Linha 7: peças brancas (base)
    tabuleiro = []
    tabuleiro.append(["Tp", "Cp", "Bp", "Dp", "Rp", "Bp", "Cp", "Tp"])
    tabuleiro.append(["Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp"])
    for i in range(4):
        # Cada linha vazia é uma lista independente
        linha = []
        for j in range(8):
            linha.append(".")
        tabuleiro.append(linha)
    tabuleiro.append(["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"])
    tabuleiro.append(["Tb", "Cb", "Bb", "Db", "Rb", "Bb", "Cb", "Tb"])
    return tabuleiro


def tabuleiro_para_texto(tab):
    """
    Converte o tabuleiro para uma string formatada para exibição.
    Parâmetros:
        tab (list): tabuleiro 8x8.
    Retorna:
        str: representação textual do tabuleiro.
    """
    # Cabeçalho com índices das colunas
    texto = "    0  1  2  3  4  5  6  7\n"
    for i in range(8):
        # Número da linha seguido das peças alinhadas
        linha_texto = str(i) + "   "
        for j in range(8):
            linha_texto = linha_texto + tab[i][j].ljust(3)
        texto = texto + linha_texto + "\n"
    return texto


def mostrar_tabuleiro(tab):
    """
    Imprime o tabuleiro no terminal.
    Parâmetros:
        tab (list): tabuleiro 8x8.
    Retorna:
        None
    """
    print(tabuleiro_para_texto(tab))


def posicao_valida(pos):
    """
    Verifica se uma posição é válida no tabuleiro.
    Parâmetros:
        pos (tuple): posição (linha, coluna).
    Retorna:
        bool: True se a posição está dentro do tabuleiro.
    """
    # Deve ser tupla com exatamente 2 elementos inteiros, entre 0 e 7
    if not isinstance(pos, tuple):
        return False
    if len(pos) != 2:
        return False
    if not isinstance(pos[0], int) or not isinstance(pos[1], int):
        return False
    if pos[0] < 0 or pos[0] > 7:
        return False
    if pos[1] < 0 or pos[1] > 7:
        return False
    return True


def mover_peca(tab, origem, destino):
    """
    Move uma peça de origem para destino no tabuleiro.
    Não valida regras de xadrez, apenas posições e origem não-vazia.
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem (linha, coluna).
        destino (tuple): posição de destino (linha, coluna).
    Retorna:
        bool: True se o movimento foi realizado.
    """
    if not posicao_valida(origem) or not posicao_valida(destino):
        return False
    peca = tab[origem[0]][origem[1]]
    if peca == ".":
        return False
    # Copia a peça para o destino e limpa a origem
    tab[destino[0]][destino[1]] = peca
    tab[origem[0]][origem[1]] = "."
    return True


def obter_peca(tab, pos):
    """
    Retorna a peça na posição indicada.
    Parâmetros:
        tab (list): tabuleiro 8x8.
        pos (tuple): posição (linha, coluna).
    Retorna:
        str: string da peça (ex: 'Tb') ou '.' se vazia.
    """
    return tab[pos[0]][pos[1]]


def cor_da_peca(peca):
    """
    Retorna a cor de uma peça.
    Parâmetros:
        peca (str): string da peça (ex: 'Tb').
    Retorna:
        str ou None: 'b' (branca), 'p' (preta) ou None se vazia.
    """
    if peca == ".":
        return None
    return peca[1]


def tipo_da_peca(peca):
    """
    Retorna o tipo de uma peça.
    Parâmetros:
        peca (str): string da peça (ex: 'Tb').
    Retorna:
        str ou None: 'T', 'C', 'B', 'D', 'R', 'P' ou None se vazia.
    """
    if peca == ".":
        return None
    return peca[0]


def notacao_para_posicao(txt):
    """
    Converte notação algébrica (ex: 'e2') para posição (linha, coluna).
    Parâmetros:
        txt (str): notação algébrica (ex: 'e2').
    Retorna:
        tuple: posição (linha, coluna). Ex: 'e2' -> (6, 4).
    """
    # coluna: a=0, b=1, ..., h=7
    coluna = ord(txt[0]) - ord('a')
    # linha: '1'->7, '2'->6, ..., '8'->0
    linha = 8 - int(txt[1])
    return (linha, coluna)

