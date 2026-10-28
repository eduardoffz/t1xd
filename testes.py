# testes.py — Integrante 4: Testes unitários
# Importa main (que importa todos os outros módulos)

import unittest
from tabuleiro import (criar_tabuleiro, posicao_valida, mover_peca,
                       obter_peca, cor_da_peca, tipo_da_peca,
                       notacao_para_posicao, tabuleiro_para_texto)
from pecas_linha import caminho_livre, movimento_torre, movimento_bispo, movimento_dama
from capturas import (movimento_rei, movimento_cavalo, mesma_cor,
                      captura_permitida, capturar_peca)
from peao import movimento_peao, controlar_turno, trocar_turno
from main import executar_jogada, partida_demo


# ---------- Auxiliar ----------

def criar_tabuleiro_vazio():
    """
    Cria um tabuleiro 8x8 vazio (só com '.').
    Retorna:
        list: tabuleiro vazio.
    """
    tab = []
    for i in range(8):
        linha = []
        for j in range(8):
            linha.append(".")
        tab.append(linha)
    return tab


def copiar_tabuleiro(tab):
    """
    Cria uma cópia independente do tabuleiro.
    Parâmetros:
        tab (list): tabuleiro original.
    Retorna:
        list: cópia do tabuleiro.
    """
    copia = []
    for i in range(8):
        linha = []
        for j in range(8):
            linha.append(tab[i][j])
        copia.append(linha)
    return copia


# ========== 1. Testes do Tabuleiro ==========

class TestTabuleiro(unittest.TestCase):
    """Testes para o módulo tabuleiro.py"""

    def test_posicoes_iniciais(self):
        """Verifica se as peças estão nas posições iniciais corretas"""
        tab = criar_tabuleiro()
        # Peças pretas (linha 0)
        self.assertEqual(tab[0][0], "Tp")
        self.assertEqual(tab[0][1], "Cp")
        self.assertEqual(tab[0][2], "Bp")
        self.assertEqual(tab[0][3], "Dp")
        self.assertEqual(tab[0][4], "Rp")
        self.assertEqual(tab[0][5], "Bp")
        self.assertEqual(tab[0][6], "Cp")
        self.assertEqual(tab[0][7], "Tp")
        # Peões pretos (linha 1)
        for c in range(8):
            self.assertEqual(tab[1][c], "Pp")
        # Linhas vazias (2 a 5)
        for l in range(2, 6):
            for c in range(8):
                self.assertEqual(tab[l][c], ".")
        # Peões brancos (linha 6)
        for c in range(8):
            self.assertEqual(tab[6][c], "Pb")
        # Peças brancas (linha 7)
        self.assertEqual(tab[7][0], "Tb")
        self.assertEqual(tab[7][4], "Rb")
        self.assertEqual(tab[7][3], "Db")

    def test_posicao_valida(self):
        """Verifica posicao_valida com vários inputs"""
        self.assertTrue(posicao_valida((0, 0)))
        self.assertTrue(posicao_valida((7, 7)))
        self.assertTrue(posicao_valida((3, 4)))
        self.assertFalse(posicao_valida((8, 0)))
        self.assertFalse(posicao_valida((-1, 3)))
        self.assertFalse(posicao_valida((2,)))       # tupla incompleta
        self.assertFalse(posicao_valida("ab"))        # não é tupla
        self.assertFalse(posicao_valida((0, 8)))

    def test_mover_peca_valido(self):
        """Verifica mover_peca com movimento válido"""
        tab = criar_tabuleiro()
        resultado = mover_peca(tab, (6, 4), (4, 4))
        self.assertTrue(resultado)
        self.assertEqual(tab[6][4], ".")
        self.assertEqual(tab[4][4], "Pb")

    def test_mover_peca_origem_vazia(self):
        """Verifica que mover_peca retorna False para origem vazia"""
        tab = criar_tabuleiro()
        resultado = mover_peca(tab, (3, 3), (4, 3))
        self.assertFalse(resultado)

    def test_obter_peca(self):
        """Verifica obter_peca"""
        tab = criar_tabuleiro()
        self.assertEqual(obter_peca(tab, (0, 0)), "Tp")
        self.assertEqual(obter_peca(tab, (3, 3)), ".")

    def test_cor_da_peca(self):
        """Verifica cor_da_peca"""
        self.assertEqual(cor_da_peca("Tb"), "b")
        self.assertEqual(cor_da_peca("Pp"), "p")
        self.assertIsNone(cor_da_peca("."))

    def test_tipo_da_peca(self):
        """Verifica tipo_da_peca"""
        self.assertEqual(tipo_da_peca("Tb"), "T")
        self.assertEqual(tipo_da_peca("Pp"), "P")
        self.assertIsNone(tipo_da_peca("."))

    def test_notacao_para_posicao(self):
        """Verifica conversão de notação algébrica"""
        self.assertEqual(notacao_para_posicao("e2"), (6, 4))
        self.assertEqual(notacao_para_posicao("a8"), (0, 0))
        self.assertEqual(notacao_para_posicao("h1"), (7, 7))
        self.assertEqual(notacao_para_posicao("d4"), (4, 3))


# ========== 2. Testes das Peças de Linha ==========

class TestPecasLinha(unittest.TestCase):
    """Testes para o módulo pecas_linha.py (torre, bispo, dama)"""

    def test_torre_valida_sem_tab(self):
        """Torre: movimento válido na mesma linha (sem tabuleiro)"""
        self.assertTrue(movimento_torre((0, 0), (0, 5)))

    def test_torre_bloqueada_por_peca(self):
        """Torre: bloqueada por peça no caminho"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_torre((0, 0), (0, 5), tab))

    def test_torre_caminho_livre(self):
        """Torre: caminho livre em tabuleiro vazio"""
        tab_vazio = criar_tabuleiro_vazio()
        self.assertTrue(movimento_torre((4, 4), (4, 0), tab_vazio))

    def test_torre_diagonal_invalida(self):
        """Torre: diagonal é inválido"""
        self.assertFalse(movimento_torre((0, 0), (3, 3)))

    def test_bispo_valido_sem_tab(self):
        """Bispo: diagonal válida sem tabuleiro"""
        self.assertTrue(movimento_bispo((1, 1), (4, 4)))

    def test_bispo_bloqueado(self):
        """Bispo: bloqueado por peão"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_bispo((7, 2), (4, 5), tab))

    def test_bispo_mesma_linha_invalido(self):
        """Bispo: mesma linha não é diagonal"""
        self.assertFalse(movimento_bispo((4, 4), (4, 6)))

    def test_dama_diagonal_sem_tab(self):
        """Dama: diagonal válida sem tabuleiro"""
        self.assertTrue(movimento_dama((0, 0), (7, 7)))

    def test_dama_bloqueada(self):
        """Dama: bloqueada por peão"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_dama((7, 3), (4, 3), tab))

    def test_dama_formato_cavalo_invalido(self):
        """Dama: formato de cavalo é inválido"""
        self.assertFalse(movimento_dama((4, 4), (6, 5)))

    def test_caminho_livre_diagonal_vazio(self):
        """Caminho livre em diagonal no tabuleiro vazio"""
        tab_vazio = criar_tabuleiro_vazio()
        self.assertTrue(caminho_livre(tab_vazio, (0, 0), (7, 7)))

    def test_caminho_bloqueado_vertical(self):
        """Caminho bloqueado verticalmente por peão"""
        tab = criar_tabuleiro()
        self.assertFalse(caminho_livre(tab, (7, 0), (4, 0)))


# ========== 3. Testes de Capturas (Rei, Cavalo) ==========

class TestCapturas(unittest.TestCase):
    """Testes para o módulo capturas.py (rei, cavalo e capturas)"""

    def test_rei_valido(self):
        """Rei: 1 casa diagonal é válido"""
        self.assertTrue(movimento_rei((4, 4), (5, 5)))

    def test_rei_mesma_posicao(self):
        """Rei: mesma posição é inválido"""
        self.assertFalse(movimento_rei((4, 4), (4, 4)))

    def test_rei_duas_casas(self):
        """Rei: 2 casas é inválido"""
        self.assertFalse(movimento_rei((4, 4), (6, 4)))

    def test_cavalo_valido(self):
        """Cavalo: L válido"""
        self.assertTrue(movimento_cavalo((4, 4), (6, 5)))

    def test_cavalo_diagonal_invalido(self):
        """Cavalo: diagonal simples é inválido"""
        self.assertFalse(movimento_cavalo((4, 4), (5, 5)))

    def test_cavalo_pula_pecas(self):
        """Cavalo: pula peças (posição inicial)"""
        self.assertTrue(movimento_cavalo((7, 1), (5, 2)))

    def test_mesma_cor_verdadeiro(self):
        """mesma_cor: duas brancas"""
        self.assertTrue(mesma_cor("Tb", "Pb"))

    def test_mesma_cor_falso(self):
        """mesma_cor: cores diferentes"""
        self.assertFalse(mesma_cor("Tb", "Pp"))

    def test_mesma_cor_vazia(self):
        """mesma_cor: com casa vazia"""
        self.assertFalse(mesma_cor("Tb", "."))

    def test_captura_mesma_cor_impedida(self):
        """Captura impedida: peças da mesma cor"""
        tab = criar_tabuleiro()
        self.assertFalse(captura_permitida(tab, (7, 0), (6, 0)))

    def test_captura_permitida_cores_diferentes(self):
        """Captura permitida: cores diferentes"""
        tab = criar_tabuleiro_vazio()
        tab[4][0] = "Tb"
        tab[4][5] = "Pp"
        self.assertTrue(captura_permitida(tab, (4, 0), (4, 5)))

    def test_capturar_peca_realiza(self):
        """capturar_peca: realiza a captura corretamente"""
        tab = criar_tabuleiro_vazio()
        tab[4][0] = "Tb"
        tab[4][5] = "Pp"
        resultado = capturar_peca(tab, (4, 0), (4, 5))
        self.assertTrue(resultado)
        self.assertEqual(tab[4][5], "Tb")
        self.assertEqual(tab[4][0], ".")

    def test_capturar_peca_mesma_cor_falha(self):
        """capturar_peca: falha com mesma cor"""
        tab = criar_tabuleiro()
        copia = copiar_tabuleiro(tab)
        resultado = capturar_peca(tab, (7, 0), (6, 0))
        self.assertFalse(resultado)
        # Tabuleiro não muda
        for l in range(8):
            for c in range(8):
                self.assertEqual(tab[l][c], copia[l][c])


# ========== 4. Testes do Peão e Turnos ==========

class TestPeao(unittest.TestCase):
    """Testes para o módulo peao.py (peão, turnos)"""

    def test_peao_branco_1_casa(self):
        """Peão branco: avança 1 casa"""
        tab = criar_tabuleiro()
        self.assertTrue(movimento_peao(tab, (6, 4), (5, 4)))

    def test_peao_branco_2_casas(self):
        """Peão branco: avança 2 casas da posição inicial"""
        tab = criar_tabuleiro()
        self.assertTrue(movimento_peao(tab, (6, 4), (4, 4)))

    def test_peao_branco_3_casas_invalido(self):
        """Peão branco: 3 casas é inválido"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_peao(tab, (6, 4), (3, 4)))

    def test_peao_2_casas_fora_posicao_inicial(self):
        """Peão: 2 casas fora da posição inicial é inválido"""
        tab = criar_tabuleiro_vazio()
        tab[5][4] = "Pb"
        self.assertFalse(movimento_peao(tab, (5, 4), (3, 4)))

    def test_peao_bloqueado_casa_meio(self):
        """Peão: bloqueado na casa do meio ao tentar 2 casas"""
        tab = criar_tabuleiro()
        tab[5][4] = "Pb"  # peça no caminho
        self.assertFalse(movimento_peao(tab, (6, 4), (4, 4)))

    def test_peao_bloqueado_frente(self):
        """Peão: bloqueado na frente"""
        tab = criar_tabuleiro()
        tab[5][4] = "Pp"  # peça inimiga na frente
        self.assertFalse(movimento_peao(tab, (6, 4), (5, 4)))

    def test_peao_captura_diagonal(self):
        """Peão: captura diagonal válida"""
        tab = criar_tabuleiro()
        tab[5][5] = "Pp"  # peça inimiga na diagonal
        self.assertTrue(movimento_peao(tab, (6, 4), (5, 5)))

    def test_peao_diagonal_vazia_invalido(self):
        """Peão: diagonal vazia é inválido"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_peao(tab, (6, 4), (5, 5)))

    def test_peao_captura_mesma_cor_invalido(self):
        """Peão: não pode capturar peça da mesma cor"""
        tab = criar_tabuleiro()
        tab[5][5] = "Pb"  # peça da mesma cor
        self.assertFalse(movimento_peao(tab, (6, 4), (5, 5)))

    def test_peao_para_tras_invalido(self):
        """Peão branco: não pode andar para trás"""
        tab = criar_tabuleiro_vazio()
        tab[5][4] = "Pb"
        self.assertFalse(movimento_peao(tab, (5, 4), (6, 4)))

    def test_peao_lateral_invalido(self):
        """Peão: não pode andar de lado"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_peao(tab, (6, 4), (6, 5)))

    def test_peao_preto_2_casas(self):
        """Peão preto: avança 2 casas da posição inicial"""
        tab = criar_tabuleiro()
        self.assertTrue(movimento_peao(tab, (1, 3), (3, 3)))

    def test_peao_preto_para_tras(self):
        """Peão preto: não pode andar para trás"""
        tab = criar_tabuleiro()
        self.assertFalse(movimento_peao(tab, (1, 3), (0, 3)))

    def test_controlar_turno_brancas(self):
        """controlar_turno: peça branca no turno brancas"""
        self.assertTrue(controlar_turno("brancas", "Pb"))

    def test_controlar_turno_brancas_peca_preta(self):
        """controlar_turno: peça preta no turno brancas"""
        self.assertFalse(controlar_turno("brancas", "Pp"))

    def test_controlar_turno_pretas(self):
        """controlar_turno: peça preta no turno pretas"""
        self.assertTrue(controlar_turno("pretas", "Pp"))

    def test_controlar_turno_vazia(self):
        """controlar_turno: casa vazia"""
        self.assertFalse(controlar_turno("pretas", "."))

    def test_trocar_turno(self):
        """trocar_turno: alterna entre brancas e pretas"""
        self.assertEqual(trocar_turno("brancas"), "pretas")
        self.assertEqual(trocar_turno("pretas"), "brancas")


# ========== 5. Testes de Integração (executar_jogada) ==========

class TestIntegracao(unittest.TestCase):
    """Testes de integração para executar_jogada"""

    def test_jogada_posicao_invalida(self):
        """executar_jogada: posição fora do tabuleiro"""
        tab = criar_tabuleiro()
        res = executar_jogada(tab, (8, 0), (7, 0), "brancas")
        self.assertFalse(res["ok"])
        self.assertEqual(res["msg"], "Posição fora do tabuleiro")

    def test_jogada_origem_vazia(self):
        """executar_jogada: origem sem peça"""
        tab = criar_tabuleiro()
        res = executar_jogada(tab, (4, 4), (5, 4), "brancas")
        self.assertFalse(res["ok"])
        self.assertEqual(res["msg"], "Não há peça na origem")

    def test_jogada_turno_errado(self):
        """executar_jogada: jogada fora da vez"""
        tab = criar_tabuleiro()
        copia = copiar_tabuleiro(tab)
        res = executar_jogada(tab, (1, 4), (3, 4), "brancas")
        self.assertFalse(res["ok"])
        self.assertEqual(res["msg"], "Não é a vez dessa cor")
        self.assertEqual(res["turno"], "brancas")  # turno não muda
        # Tabuleiro inalterado
        for l in range(8):
            for c in range(8):
                self.assertEqual(tab[l][c], copia[l][c])

    def test_jogada_mesma_origem_destino(self):
        """executar_jogada: origem igual ao destino"""
        tab = criar_tabuleiro()
        res = executar_jogada(tab, (6, 4), (6, 4), "brancas")
        self.assertFalse(res["ok"])

    def test_jogada_peao_valida(self):
        """executar_jogada: peão avança 2 casas"""
        tab = criar_tabuleiro()
        res = executar_jogada(tab, (6, 4), (4, 4), "brancas")
        self.assertTrue(res["ok"])
        self.assertEqual(res["turno"], "pretas")
        self.assertEqual(tab[4][4], "Pb")

    def test_jogada_torre_obstruida(self):
        """executar_jogada: torre obstruída pelo peão"""
        tab = criar_tabuleiro()
        res = executar_jogada(tab, (7, 0), (5, 0), "brancas")
        self.assertFalse(res["ok"])
        self.assertEqual(res["msg"], "Caminho obstruído")

    def test_jogada_destino_mesma_cor(self):
        """executar_jogada: destino ocupado por mesma cor"""
        tab = criar_tabuleiro()
        # Mover peão para liberar cavalo, depois tentar cavalo para peão
        tab[5][0] = "."  # remove peão para abrir espaço de teste
        tab[5][0] = "Pb"  # coloca peão branco onde cavalo tentaria ir
        # Cavalo em (7,1) tenta ir para (5,0) onde há Pb
        res = executar_jogada(tab, (7, 1), (5, 0), "brancas")
        self.assertFalse(res["ok"])
        self.assertEqual(res["msg"], "Destino ocupado por peça da mesma cor")


# ========== 6. Testes da Demo ==========

class TestDemo(unittest.TestCase):
    """Testes da partida demo"""

    def test_demo_quantidade_jogadas(self):
        """partida_demo: tem 15 jogadas (12 válidas + 3 inválidas)"""
        passos = partida_demo()
        self.assertEqual(len(passos), 15)

    def test_demo_jogadas_validas(self):
        """partida_demo: pelo menos 10 jogadas válidas"""
        passos = partida_demo()
        validas = 0
        for passo in passos:
            if passo["resultado"]["ok"]:
                validas = validas + 1
        self.assertGreaterEqual(validas, 10)

    def test_demo_capturas(self):
        """partida_demo: pelo menos 1 captura"""
        passos = partida_demo()
        capturas = 0
        for passo in passos:
            if passo["resultado"]["captura"]:
                capturas = capturas + 1
        self.assertGreaterEqual(capturas, 1)

    def test_demo_jogadas_invalidas(self):
        """partida_demo: pelo menos 1 jogada inválida"""
        passos = partida_demo()
        invalidas = 0
        for passo in passos:
            if not passo["resultado"]["ok"]:
                invalidas = invalidas + 1
        self.assertGreaterEqual(invalidas, 1)


if __name__ == "__main__":
    unittest.main()

