# main.py — Integração: executar_jogada + partida demo (CLI)
# Importa todos os módulos do projeto

from tabuleiro import (criar_tabuleiro, mostrar_tabuleiro, tabuleiro_para_texto,
                       posicao_valida, mover_peca, obter_peca, cor_da_peca,
                       tipo_da_peca, notacao_para_posicao)
from pecas_linha import movimento_torre, movimento_bispo, movimento_dama
from capturas import movimento_rei, movimento_cavalo, mesma_cor, capturar_peca
from peao import movimento_peao, controlar_turno, trocar_turno


def executar_jogada(tab, origem, destino, turno):
    """
    Executa uma jogada completa com todas as validações.
    Ordem das verificações (para na primeira que falhar):
    1. Posições válidas
    2. Peça na origem
    3. Turno correto
    4. Movimento válido para o tipo da peça
    5. Destino não ocupado por peça da mesma cor
    6. Captura ou movimento simples
    7. Troca de turno
    Parâmetros:
        tab (list): tabuleiro 8x8.
        origem (tuple): posição de origem.
        destino (tuple): posição de destino.
        turno (str): 'brancas' ou 'pretas'.
    Retorna:
        dict: {'ok': bool, 'msg': str, 'captura': bool, 'turno': str}
    """
    # 1. Verificar posições válidas
    if not posicao_valida(origem) or not posicao_valida(destino):
        return {"ok": False, "msg": "Posição fora do tabuleiro", "captura": False, "turno": turno}

    # 2. Verificar se há peça na origem
    peca = obter_peca(tab, origem)
    if peca == ".":
        return {"ok": False, "msg": "Não há peça na origem", "captura": False, "turno": turno}

    # 3. Verificar turno
    if not controlar_turno(turno, peca):
        return {"ok": False, "msg": "Não é a vez dessa cor", "captura": False, "turno": turno}

    # 4. Verificar movimento válido conforme o tipo da peça
    tipo = tipo_da_peca(peca)

    if tipo == "T":
        # Geometria sem tabuleiro
        if not movimento_torre(origem, destino):
            return {"ok": False, "msg": "Movimento inválido para a peça", "captura": False, "turno": turno}
        # Geometria com tabuleiro (verifica obstrução)
        if not movimento_torre(origem, destino, tab):
            return {"ok": False, "msg": "Caminho obstruído", "captura": False, "turno": turno}
    elif tipo == "B":
        if not movimento_bispo(origem, destino):
            return {"ok": False, "msg": "Movimento inválido para a peça", "captura": False, "turno": turno}
        if not movimento_bispo(origem, destino, tab):
            return {"ok": False, "msg": "Caminho obstruído", "captura": False, "turno": turno}
    elif tipo == "D":
        if not movimento_dama(origem, destino):
            return {"ok": False, "msg": "Movimento inválido para a peça", "captura": False, "turno": turno}
        if not movimento_dama(origem, destino, tab):
            return {"ok": False, "msg": "Caminho obstruído", "captura": False, "turno": turno}
    elif tipo == "R":
        if not movimento_rei(origem, destino):
            return {"ok": False, "msg": "Movimento inválido para a peça", "captura": False, "turno": turno}
    elif tipo == "C":
        if not movimento_cavalo(origem, destino):
            return {"ok": False, "msg": "Movimento inválido para a peça", "captura": False, "turno": turno}
    elif tipo == "P":
        if not movimento_peao(tab, origem, destino):
            return {"ok": False, "msg": "Movimento inválido do peão", "captura": False, "turno": turno}

    # 5. Verificar se destino tem peça da mesma cor
    peca_destino = obter_peca(tab, destino)
    if peca_destino != "." and mesma_cor(peca, peca_destino):
        return {"ok": False, "msg": "Destino ocupado por peça da mesma cor", "captura": False, "turno": turno}

    # 6. Realizar o movimento ou captura
    captura = False
    if peca_destino != "." and not mesma_cor(peca, peca_destino):
        # Captura
        capturar_peca(tab, origem, destino)
        captura = True
    else:
        # Movimento simples
        mover_peca(tab, origem, destino)

    # 7. Trocar turno
    novo_turno = trocar_turno(turno)
    if captura:
        return {"ok": True, "msg": "Captura realizada", "captura": True, "turno": novo_turno}
    return {"ok": True, "msg": "Jogada realizada", "captura": False, "turno": novo_turno}


def partida_demo():
    """
    Executa uma partida demo com sequência pré-definida de jogadas.
    Retorna:
        list: lista de dicts com turno, origem_txt, destino_txt, resultado, tabuleiro_texto.
    """
    tab = criar_tabuleiro()
    turno = "brancas"
    passos = []

    # Sequência de jogadas da demo
    jogadas = [
        ("e2", "e4"),   # 1. brancas - peão 2 casas
        ("e7", "e5"),   # 2. pretas - peão
        ("g1", "f3"),   # 3. brancas - cavalo
        ("b8", "c6"),   # 4. pretas - cavalo
        ("a1", "a4"),   # X. brancas - torre (caminho obstruído)
        ("f1", "c4"),   # 5. brancas - bispo
        ("g8", "f6"),   # 6. pretas - cavalo
        ("d1", "e2"),   # 7. brancas - dama
        ("f8", "c5"),   # 8. pretas - bispo
        ("e1", "f1"),   # 9. brancas - rei
        ("h8", "g8"),   # 10. pretas - torre
        ("f3", "e5"),   # 11. brancas - cavalo captura peão preto
        ("c6", "e5"),   # 12. pretas - cavalo captura cavalo branco
        ("a1", "a2"),   # X. brancas - torre (destino ocupado mesma cor)
        ("d7", "d5"),   # X. brancas - peão preto (não é a vez)
    ]

    for jogada in jogadas:
        origem_txt = jogada[0]
        destino_txt = jogada[1]
        origem = notacao_para_posicao(origem_txt)
        destino = notacao_para_posicao(destino_txt)
        resultado = executar_jogada(tab, origem, destino, turno)

        passo = {
            "turno": turno,
            "origem_txt": origem_txt,
            "destino_txt": destino_txt,
            "resultado": resultado,
            "tabuleiro_texto": tabuleiro_para_texto(tab)
        }
        passos.append(passo)

        # Só atualiza o turno se a jogada foi válida
        if resultado["ok"]:
            turno = resultado["turno"]

    return passos


def rodar_demo_terminal():
    """
    Executa a partida demo e imprime cada passo no terminal.
    Retorna:
        None
    """
    passos = partida_demo()
    print("=" * 50)
    print("  PARTIDA DEMO - XADREZ SIMPLIFICADO")
    print("=" * 50)
    print()

    for i in range(len(passos)):
        passo = passos[i]
        resultado = passo["resultado"]
        status = "OK" if resultado["ok"] else "FALHOU"
        print(f"Jogada: {passo['origem_txt']} -> {passo['destino_txt']}  "
              f"(Turno: {passo['turno']}) [{status}] {resultado['msg']}")
        mostrar_tabuleiro_do_texto(passo["tabuleiro_texto"])
        print()


def mostrar_tabuleiro_do_texto(texto):
    """
    Imprime o texto do tabuleiro.
    Parâmetros:
        texto (str): representação textual do tabuleiro.
    Retorna:
        None
    """
    print(texto)


if __name__ == "__main__":
    rodar_demo_terminal()

